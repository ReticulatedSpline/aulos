"""classes responsible for the user interface"""
import os
import sys
import curses
from datetime import timedelta
import cfg
from typing import NamedTuple, List
from enum import IntEnum


class ItemType(IntEnum):
    """home menu options"""
    Menu = 0
    Directory = 1
    Playlist = 2
    Track = 3


class DisplayItem(NamedTuple):
    item_type: ItemType
    path: str


class Display(NamedTuple):
    """hold all information necessary to draw a display"""
    items: List[DisplayItem]
    menu_path: str = ''
    index: int = 0
    start_index: int = 0

    def get_selected_item(self):
        if len(self.items) > 0:
            return self.items[self.index + self.start_index]
        else:
            return None


class View:
    """wrap the curses library and handle the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(False)

        self.menu_stack = list()
        home_items = list()
        for item in cfg.home_menu_items:
            home_items.append(DisplayItem(ItemType.Menu, item))
        self.menu_stack.append(Display(home_items, ''))

        # persistant screen locations
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()
        self.num_menu_lines = self.max_y_chars - 7
        self.y_indicies = {
            'status': self.max_y_chars - 5,
            'metadata': self.max_y_chars - 4,
            'time': self.max_y_chars - 3,
            'progress_bar': self.max_y_chars - 2
        }

        self.update_menu()
        self.update_status(None)

    def __del__(self):
        """restore the previous state of the terminal"""
        curses.endwin()
        # cross-platform console clear
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _strfdelta(tdelta: timedelta) -> str:
        """format a timedelta into a string"""
        days = tdelta.days
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        time_str = f'{minutes}:{seconds:0>2}'
        if days > 0:
            time_str += str(days) + ' days, '
        if hours > 0:
            time_str += str(hours) + ' hours '
        return time_str

    def _clear_line(self, line: int):
        self.screen.move(line, 1)
        self.screen.clrtoeol()
        self._draw_borders()

    def _clear_menu_lines(self):
        for line in list(range(1, self.num_menu_lines + 1)):
            self._clear_line(line)

    def _clear_status_lines(self):
        self._clear_line(self.y_indicies['metadata'])
        self._clear_line(self.y_indicies['time'])
        self._clear_line(self.y_indicies['progress_bar'])

    def _truncate_string(self, string: str) -> str:
        # four from two border chars and two box drawing chars
        available_space = self.max_x_chars - 4
        if len(string) < available_space:
            return string
        else:
            string = os.path.basename(string)

        str_len = len(string)
        if str_len > available_space:
            start = (str_len - available_space) + 3  # three for ellipsis
            string = '...' + string[start:]
        return string

    def _draw_borders(self):
        self.screen.border(0)
        menu_path = self.menu_stack[-1].menu_path
        if not menu_path:
            title = ' ' + cfg.home_icon + ' '
        else:
            title = ' ' + menu_path + ' '
        title = self._truncate_string(title)
        title_pos = (self.max_x_chars - len(title)) // 2
        self.screen.addstr(0, title_pos, title)
        self.screen.addch(0, title_pos - 1, curses.ACS_RTEE)
        self.screen.addch(0, title_pos + len(title), curses.ACS_LTEE)
        middle_border = self.y_indicies['status'] - 1
        # draw connecting characters from extended curses set
        self.screen.addch(middle_border, 0, curses.ACS_LTEE)
        self.screen.addch(middle_border, self.max_x_chars - 1, curses.ACS_RTEE)
        # draw middle border line
        self.screen.hline(middle_border, 1, curses.ACS_HLINE,
                          self.max_x_chars - 2)

    def _draw_progress_bar(self, metadata: dict):
        if metadata is None:
            run_time = 0
            curr_time = 0
        else:
            run_time = metadata.get('run_time')
            curr_time = metadata.get('curr_time')

        progress_bar_chars = self.max_x_chars - 2
        if run_time == 0:
            percent = 0
            fill_count = 0
            void_count = progress_bar_chars
        else:
            percent = int((curr_time / run_time) * 100)
            fill_count = int(progress_bar_chars * curr_time / run_time)
            void_count = progress_bar_chars - fill_count

        run_time_str = self._strfdelta(timedelta(seconds=run_time))
        curr_time_str = self._strfdelta(timedelta(seconds=curr_time))
        percent_str = ' (' + str(percent) + '%)'
        time_str = curr_time_str + cfg.time_sep_str + run_time_str
        time_str += percent_str

        # two border characters
        progress_fill = cfg.progress_bar_fill_char * fill_count
        progress_void = cfg.progress_bar_empty_char * void_count
        progress_bar = progress_fill + progress_void

        self.screen.addstr(self.y_indicies['time'], 1, time_str)
        self.screen.addstr(self.y_indicies['progress_bar'], 1, progress_bar)

    def draw_empty_str(self):
        """denote an empty collection of display items"""
        self.screen.addstr(1, 1, cfg.empty_str)

    def navigate_up(self):
        display = self.menu_stack[-1]
        if display.start_index + display.index > 0:
            self.menu_stack.pop()
            index = display.index
            start_index = display.start_index
            if display.index > 0:
                index = display.index - 1
            elif display.start_index >= self.num_menu_lines:
                start_index = start_index - self.num_menu_lines
                index = self.num_menu_lines - 1
            display = display._replace(index=index, start_index=start_index)
            self.menu_stack.append(display)

    def navigate_down(self):
        display = self.menu_stack[-1]
        if display.start_index + display.index < len(display.items) - 1:
            display = self.menu_stack.pop()
            display = display._replace(index=display.index + 1)
            if display.index >= self.num_menu_lines:
                start_index = display.start_index + self.num_menu_lines
                display = display._replace(index=0, start_index=start_index)
            self.menu_stack.append(display)

    def navigate_back(self):
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()

    def notify(self, string: str):
        """add a string to the window; persistant until overwritten"""
        self._clear_line(self.y_indicies['status'])
        self.screen.addstr(self.y_indicies['status'], 1, string)

    def update_menu(self):
        """draw the top menu on the menu stack"""
        self._clear_menu_lines()
        display = self.menu_stack[-1]

        if not display.items:
            self.draw_empty_str()
            return

        display_items = display.items[display.start_index:]
        if len(display_items) <= 0:
            self.draw_empty_str()
        else:
            for list_index, item in enumerate(display_items, start=1):
                if list_index > self.num_menu_lines:
                    break
                item_name = os.path.basename(item.path)
                item_name = self._truncate_string(item_name)
                if item.item_type is ItemType.Menu:
                    item_name = cfg.menu_icon + item_name
                elif item.item_type is ItemType.Directory:
                    item_name = cfg.dir_icon + item_name
                elif item.item_type is ItemType.Playlist:
                    item_name = cfg.playlist_icon + item_name
                elif item.item_type is ItemType.Track:
                    item_name = cfg.track_icon + item_name

                if display.index + 1 == list_index:
                    self.screen.addstr(list_index, 1, item_name, curses.A_REVERSE)
                else:
                    self.screen.addstr(list_index, 1, item_name)

    def update_status(self, metadata: dict):
        """update track metadata and progress indicators."""

        self._clear_status_lines()
        if metadata is None:
            self.notify(cfg.no_media_str)
            self.screen.addstr(self.y_indicies['metadata'], 1, cfg.no_load_str)
        else:
            title = metadata.get('title')[0]
            artist = metadata.get('artist')[0]
            track_info = title + cfg.track_sep_str + artist
            self.screen.addstr(self.y_indicies['metadata'], 1, track_info)
        self._draw_progress_bar(metadata)
