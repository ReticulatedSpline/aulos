import cfg
import curses
import glob
from enum import IntEnum
from datetime import timedelta


class Menu(IntEnum):
    PLAYLISTS = 1
    ALBUMS = 2
    ARTISTS = 3
    GENRES = 4
    TRACKS = 5
    QUEUE = 6
    SETTINGS = 7
    EXIT = 8


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
        # number of rows not taken up by borders or current song info
        self.free_y_chars = self.max_y_chars - 6
        self.menu_loc = 1

        # y positions of persistant screen elements
        self.status_y_loc = self.max_y_chars - 5
        self.metadata_y_loc = self.max_y_chars - 4
        self.time_y_loc = self.max_y_chars - 3
        self.prog_y_loc = self.max_y_chars - 2

        self.notify("Ready")
        self._draw_home_menu()
        self._draw_borders()
        self.update_ui(None)

    def __del__(self):
        """Restore the previous state of the terminal"""
        curses.curs_set(1)
        curses.endwin()

    def _draw_borders(self):
        self.screen.border(0)
        title_pos = (self.max_x_chars - len(cfg.title_str)) // 2
        self.screen.addstr(0, title_pos, cfg.title_str)
        middle_border_y_loc = self.status_y_loc - 1
        # draw connecting characters from extended curses set
        self.screen.addch(middle_border_y_loc, 0, curses.ACS_LTEE)
        self.screen.addch(middle_border_y_loc, self.max_x_chars - 1, curses.ACS_RTEE)
        # draw middle border line
        self.screen.hline(middle_border_y_loc, 1, curses.ACS_HLINE, self.max_x_chars - 2)

    def _clear_line(self, line: int):
        self.screen.move(line, 1)
        self.screen.clrtoeol()
        self._draw_borders()

    def _clear_menu_lines(self):
        for line in list(range(1, self.free_y_chars)):
            self._clear_line(line)
        self.screen.refresh()

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
        for idx, menu_item in enumerate(cfg.home_menu_items, start=1):
            # white space is full width with menu item and border subtracted
            white_space = ' ' * (self.max_x_chars - len(menu_item) - 2)
            if idx == self.menu_loc:  # invert color of selected item
                self.screen.addstr(idx, 1, menu_item + white_space, curses.A_REVERSE)
            else:
                self.screen.addstr(idx, 1, menu_item + white_space)
        self.screen.refresh()

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

    def _draw_playlists(self):
        self._clear_menu_lines()

        playlists = glob.glob(cfg.playlist_dir)
        for idx, playlist in enumerate(playlists, start=1):
            self.screen.addstr(idx, 1, str(playlist))
        self.screen.refresh()

    def notify(self, string: str):
        """Add a string to the window. Persistant until overwritten"""
        self._clear_line(self.status_y_loc)
        self.screen.addstr(self.status_y_loc, 1, string)
        self.screen.refresh()

    def navigate(self, direction: Direction):
        """Handle a menu selection. Returns False if exiting program, else True."""
        if direction is Direction.UP:
            if self.menu_loc > 1:
                self.menu_loc = self.menu_loc - 1
        elif direction is Direction.DOWN:
            if self.menu_loc < len(cfg.home_menu_items):
                self.menu_loc = self.menu_loc + 1
        elif direction is Direction.SELECT:
            if self.menu_loc == Menu.EXIT:
                return False
            elif self.menu_loc == Menu.PLAYLISTS:
                self._draw_playlists()
            elif self.menu_loc == Menu.ALBUMS:
                self.notify("Not yet implemented!")
            elif self.menu_loc == Menu.ARTISTS:
                self.notify("Not yet implemented!")
            elif self.menu_loc == Menu.GENRES:
                self.notify("Not yet implemented!")
            elif self.menu_loc == Menu.TRACKS:
                self.notify("Not yet implemented!")
            elif self.menu_loc == Menu.QUEUE:
                self.notify("Not yet implemented!")
            elif self.menu_loc == Menu.SETTINGS:
                self.notify("Not yet implemented!")
        elif direction is Direction.BACK:
            self._draw_home_menu()
        return True

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
        self._draw_borders()
        self.screen.refresh()
