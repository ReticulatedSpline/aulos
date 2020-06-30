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
    index: int = 0  # selected item indexed from screen start
    start_index: int = 0  # position in list to start displayed fields

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

        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()
        # 7 from 3 border chars + four status lines
        self.num_menu_lines = self.max_y_chars - 7
        # persistant screen locations
        self.y_indicies = {
            'status': self.max_y_chars - 5,
            'metadata': self.max_y_chars - 4,
            'time': self.max_y_chars - 3,
            'progress_bar': self.max_y_chars - 2
        }
        self.notify(cfg.no_media_str)

    def __del__(self):
        """restore the previous state of the terminal"""
        curses.endwin()
        # cross-platform console clear
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _strfdelta(tdelta: timedelta) -> str:
        """format a timedelta into a string"""
        if not isinstance(tdelta, timedelta):
            return cfg.no_time_str

        days = tdelta.days
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        min_sec_str = f'{minutes}:{seconds:0>2}'
        time_str = ""
        if days > 0:
            time_str += str(days) + cfg.day_str
        if hours > 0:
            time_str += str(hours) + cfg.hour_str
        return time_str + min_sec_str

    @staticmethod
    def _truncate_string(string: str, num_chars: int) -> str:
        """cut front characters with an elipsis to fit into available space"""
        if string is None or num_chars < 0:
            return ""
        elif len(string) < num_chars:
            return string

        str_len = len(string)
        if str_len > num_chars:
            start = (str_len - num_chars) + 3  # three for ellipsis
            string = '...' + string[start:]
        return string

    @staticmethod
    def _draw_progress_bar(run_time: int, curr_time: int, max_len: int):
        """return a textual progress bar spanning max_len"""
        if max_len <= 0:
            return None
        elif (run_time <= 0) or (curr_time < 0):
            fill_count = 0
            void_count = max_len
        elif run_time < curr_time:
            fill_count = max_len
            void_count = 0
        else:
            fill_count = int(max_len * curr_time / run_time)
            void_count = max_len - fill_count

        progress_fill = cfg.progress_bar_fill_char * fill_count
        progress_void = cfg.progress_bar_empty_char * void_count
        return progress_fill + progress_void

    @staticmethod
    def _draw_time_str(run_time: int, curr_time: int) -> str:
        run_time_str = View._strfdelta(timedelta(seconds=run_time))
        curr_time_str = View._strfdelta(timedelta(seconds=curr_time))
        if run_time > 0:
            percent = int((curr_time / run_time) * 100)
        else:
            percent = 0
        percent_str = ' (' + str(percent) + '%)'
        time_str = curr_time_str + cfg.time_sep_str + run_time_str
        return time_str + percent_str

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

    def _draw_borders(self):
        self.screen.border(0)
        menu_path = self.menu_stack[-1].menu_path
        if not menu_path:
            title = ' ' + cfg.home_icon + ' '
        else:
            title = ' ' + menu_path + ' '
        #  4 from two boarder characters on each side
        title = self._truncate_string(title, self.max_x_chars - 4)
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
                item_name = self._truncate_string(item_name, self.max_x_chars - 4)
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
            self.screen.addstr(self.y_indicies['metadata'], 1, cfg.no_load_str)
            run_time = curr_time = 0
        else:
            title = metadata.get('title')[0]
            artist = metadata.get('artist')[0]
            run_time = metadata.get('run_time', 0)
            curr_time = metadata.get('curr_time', 0)
            track_info = title + cfg.track_sep_str + artist
            self.screen.addstr(self.y_indicies['metadata'], 1, track_info)

        # two border characters
        width = self.max_x_chars - 2
        progress_bar = self._draw_progress_bar(run_time, curr_time, width)
        time_str = self._draw_time_str(run_time, curr_time)
        self.screen.addstr(self.y_indicies['time'], 1, time_str)
        self.screen.addstr(self.y_indicies['progress_bar'], 1, progress_bar)