import cfg  # settings
import curses  # textual user interface
from datetime import timedelta
from enum import IntEnum


class Menus(IntEnum):
    HOME = 1
    PLAYLISTS = 2
    ALBUMS = 3
    ARTISTS = 4
    GENRES = 5
    TRACKS = 6
    SETTINGS = 7


class Direction(IntEnum):
    UP = 1
    DOWN = 2
    SELECT = 3
    BACK = 4


class View:
    """Wrap the python Curses library and handle all aspects of the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)  # make the cursor invisible
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()
        self.menu_loc = 0

        # y positions of persistant screen elements
        self.status_y_loc = self.max_y_chars - 5
        self.metadata_y_loc = self.max_y_chars - 4
        self.time_y_loc = self.max_y_chars - 3
        self.prog_y_loc = self.max_y_chars - 2

        self.notify("Ready")
        self._draw_home_menu()
        self._draw_border()
        self.update_ui(None)

    def __del__(self):
        """Restore the previous state of the terminal"""
        curses.curs_set(1)
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
        for idx, menu_item in enumerate(cfg.home_menu_items):
            if idx == self.menu_loc:  # invert color of selected item
                self.screen.addstr(y_loc, 1, menu_item, curses.A_REVERSE)
            else:
                self.screen.addstr(y_loc, 1, menu_item)
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

    def navigate(self, direction: Direction):
        if direction is Direction.UP:
            if self.menu_loc > 0:
                self.menu_loc = self.menu_loc - 1
        elif direction is Direction.DOWN:
            if self.menu_loc < len(cfg.home_menu_items):
                self.menu_loc = self.menu_loc + 1
        elif direction is Direction.SELECT:
            # TODO
            pass
        elif direction is Direction.BACK:
            # TODO
            pass

    def update_ui(self, metadata: dict):
        """Update track metadata and progress indicators."""

        self._clear_line(self.metadata_y_loc)
        self._clear_line(self.time_y_loc)
        self._clear_line(self.prog_y_loc)

        if (metadata is None) or (not metadata['playing']):
            self.screen.addstr(self.metadata_y_loc, 1, cfg.no_media_str)
            self.screen.addstr(self.prog_y_loc, 1, cfg.no_load_str)
            self.screen.addstr(self.time_y_loc, 1, cfg.no_load_str)
        else:
            song_info = metadata['title'] + cfg.song_sep_str + metadata['artist']
            self.screen.addstr(self.metadata_y_loc, 1, song_info)
            self._draw_progress_info(metadata)
        self._draw_border()
        self._draw_home_menu()
        self.screen.refresh()
