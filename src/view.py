"""classes responsible for the user interface"""
import os
import curses
from typing import NamedTuple
from datetime import timedelta
import cfg


class Display(NamedTuple):
    """hold all information necessary to draw a display"""
    items: list
    menu_path: str = ''
    index: int = 0
    start_index: int = 0

    def get_selected_item(self):
        return self.items[self.index + self.start_index]

    def __str__(self):
        str_rep = f'display "{self.menu_path}" has {len(self.items)} items. '
        str_rep += f'starting at {self.start_index}, ({self.index} selected). '
        return str_rep


class View:
    """wrap the curses library and handle the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(False)

        # appended to when digging into menus, popped when navigating back
        self.menu_stack = list()
        self.menu_changed: bool = False
        home = Display([('m', item) for item in cfg.home_menu_items])
        self.menu_stack.append(home)

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

    @staticmethod
    def _strfdelta(tdelta: timedelta):
        """Format a timedelta into a string"""
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

    def _clear_progress_lines(self):
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

    def _draw_progress_info(self, metadata):
        if metadata is None:
            return

        run_time = metadata["run_time"]
        curr_time = metadata["curr_time"]

        if run_time == 0:
            return

        percent = int((curr_time / run_time) * 100)
        run_time_str = self._strfdelta(timedelta(seconds=run_time))
        curr_time_str = self._strfdelta(timedelta(seconds=curr_time))
        percent_str = ' (' + str(percent) + '%)'
        time_str = curr_time_str + cfg.time_sep_str + run_time_str
        time_str += percent_str

        # two border characters
        progress_bar_chars = self.max_x_chars - 2
        fill_count = int(progress_bar_chars * curr_time / run_time)
        progress_fill = cfg.prog_fill * fill_count
        progress_void = ' ' * (progress_bar_chars - fill_count)
        progress_bar = progress_fill + progress_void

        self.screen.addstr(self.y_indicies['time'], 1, time_str)
        self.screen.addstr(self.y_indicies['progress_bar'], 1, progress_bar)

    def navigate_up(self, display: Display):
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

    def navigate_down(self, display: Display):
        if display.start_index + display.index < len(display.items) - 1:
            display = self.menu_stack.pop()
            display = display._replace(index=display.index + 1)
            if display.index >= self.num_menu_lines:
                start_index = display.start_index + self.num_menu_lines
                display = display._replace(index=0, start_index=start_index)
        self.menu_stack.append(display)

    def notify(self, string: str):
        """add a string to the window; persistant until overwritten"""
        self._clear_line(self.y_indicies['status'])
        self.screen.addstr(self.y_indicies['status'], 1, string)
        self.screen.refresh()

    def update_menu(self):
        """draw the top menu on the menu stack"""
        self._clear_menu_lines()
        display = self.menu_stack[-1]

        if not display.items:
            return

        display_items = display.items[display.start_index:]
        for list_index, item in enumerate(display_items, start=1):
            if list_index > self.num_menu_lines:
                break
            display_name = os.path.basename(item[1])
            item_type = item[0]

            if item_type == 'm':
                display_name = cfg.menu_icon + display_name
            elif item_type == 'd':
                display_name = cfg.dir_icon + display_name
            elif item_type == 'p':
                display_name = cfg.playlist_icon + display_name
            elif item_type == 't':
                display_name = cfg.track_icon + display_name

            if display.index + 1 == list_index:
                self.screen.addstr(list_index, 1, display_name, curses.A_REVERSE)
            else:
                self.screen.addstr(list_index, 1, display_name)
        self.menu_changed = False

    def update_status(self, metadata: dict):
        """Update track metadata and progress indicators."""

        self._clear_progress_lines()
        if (metadata is None) or (not metadata['playing']):
            self.screen.addstr(
                self.y_indicies['metadata'], 1, cfg.no_media_str)
            self.screen.addstr(
                self.y_indicies['progress_bar'], 1, cfg.no_load_str)
            self.screen.addstr(self.y_indicies['time'], 1, cfg.no_load_str)
        else:
            song_info = metadata['title'] + \
                cfg.song_sep_str + metadata['artist']
            self.screen.addstr(self.y_indicies['metadata'], 1, song_info)
            self._draw_progress_info(metadata)
        self.screen.refresh()
