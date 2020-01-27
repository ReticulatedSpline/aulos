import cfg  # settings
import curses  # textual user interface
from datetime import timedelta
from enum import Enum


class Menus(Enum):
    HOME = 1
    SETTINGS = 2
    PLAYLISTS = 4
    ALBUMS = 5
    ARTISTS = 6
    GENRES = 7
    TRACKS = 8


class View:
    """Wrap the python Curses library and handle all aspects of the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)  # make the cursor invisible
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()
        self.menu_loc = 0
        self.menu_stack = list()

        # y positions of persistant screen elements
        self.screen.hline('-', self.max_y_chars - 6, 1)
        self.status_y_loc = self.max_y_chars - 5
        self.metadata_y_loc = self.max_y_chars - 4
        self.time_y_loc = self.max_y_chars - 3
        self.prog_y_loc = self.max_y_chars - 2

        self.notify("Initialized.")
        self._draw_home_menu()
        self._draw_border()
        self.screen.refresh()

    def __del__(self):
        """Restore the previous state of the terminal"""
        curses.endwin()

    def _draw_border(self):
        self.screen.border(0)
        title_pos = (self.max_x_chars - len(cfg.title_str)) // 2
        self.screen.addstr(0, title_pos, cfg.title_str)

    def _clear_line(self, line: int):
        self.screen.move(line, 1)
        self.screen.clrtoeol()
        self._draw_border()

    def _strfdelta(self, tdelta: timedelta):
        """Format a timedelta into a string"""
        days = tdelta.days
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        time_str = ''
        if days > 0:
            time_str += str(days) + ' days, '
        if hours > 0:
            time_str += str(hours) + ' hours '
        time_str += str(minutes)
        time_str += f'{minutes}:{seconds:0>2}'
        return time_str

    def _draw_home_menu(self):
        y_loc = 1
        for menu in cfg.home_menu_str:
            self.screen.addstr(y_loc, 1, menu)
            y_loc += 1

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
        time_str = curr_time_str + cfg.time_sep_str + run_time_str + percent_str

        # two border characters
        progress_bar_chars = self.max_x_chars - 2
        fill_count = int(progress_bar_chars * curr_time / run_time)
        progress_fill = cfg.prog_fill * fill_count
        progress_void = ' ' * (progress_bar_chars - fill_count)
        progress_bar = progress_fill + progress_void

        self.screen.addstr(self.time_y_loc, 1, time_str)
        self.screen.addstr(self.prog_y_loc, 1, progress_bar)

    def notify(self, string: str):
        """Add a string to the window. Persistant until overwritten"""
        self._clear_line(self.status_y_loc)
        self.screen.addstr(self.status_y_loc, 1, string)
        self.screen.refresh()

    def update_ui(self, metadata: dict):
        """Update track metadata and progress indicators."""

        self._clear_line(self.metadata_y_loc)
        self._clear_line(self.time_y_loc)
        self._clear_line(self.prog_y_loc)

        if metadata is None:
            return
        else:
            if metadata['playing']:
                song_info = metadata['title'] + cfg.song_sep_str + metadata['artist']
                self.screen.addstr(self.metadata_y_loc, 1, song_info)
            self._draw_progress_info(metadata)
        self._draw_border()
        self.screen.refresh()
