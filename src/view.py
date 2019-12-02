import cfg  # settings
import curses  # textual user interface
import datetime
from time import strftime, gmtime  # friendlier timestamps

version = '0.0.0.1'
title = 'OpenDAP' + ' ' + version
no_media_en = "Nothing is playing!"
no_progress_en = "Cannot display progress."


class View:
    """Wrap the python Curses library and handle all aspects of the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()

        self.__draw_border()

        self.screen.addstr(self.max_y_chars - 4, 1, no_media_en)
        self.screen.addstr(self.max_y_chars - 3, 1, no_progress_en)
        self.screen.addstr(self.max_y_chars - 2, 1, cfg.prompt)

        self.screen.refresh()

    def __del__(self):
        """Restore the previous state of the terminal"""
        curses.endwin()

    def __draw_border(self):
        self.screen.border(0)
        self.screen.addstr(0, (self.max_x_chars - len(title)) // 2, title)

    def __set_cursor(self):
        self.screen.move(self.max_y_chars - 2, len(cfg.prompt) + 2)

    def __clear_line(self, line: int):
        self.screen.move(line, 1)
        self.screen.clrtoeol()
        self.__draw_border()

    def __build_progress_str(self, metadata):
        run_time = metadata["run_time"]
        current_time = metadata["curr_time"]
        if (not current_time) or run_time < 0:
            return '[]'
        curr_time_str = strftime("%H:%M:%S", gmtime(current_time * 3600))
        run_time_str = strftime("%H:%M:%S", gmtime(run_time // 1000))
        percent = (current_time * 3600) // (run_time // 1000)
        print (str(run_time) + ' ' + str(current_time) + ' ' + str(percent))
        time_str = curr_time_str + cfg.time_sep + \
            run_time_str + ' ' + str(percent) + '%'
        fill_count = int(percent * 15)
        progress_fill = cfg.prog_fill * fill_count
        progress_void = ' ' * (15 - fill_count)
        return'[' + progress_fill + progress_void + '] ' + time_str

    def notify(self, string: str):
        """Add a string to the top of the window."""
        self.__clear_line(1)
        self.screen.addstr(1, 1, string)
        self.__set_cursor()
        self.screen.refresh()

    def update_ui(self, metadata: dict):
        """Update track metadata and progress indicators."""
        line1 = self.max_y_chars - 4
        line2 = self.max_y_chars - 3

        self.__clear_line(line1)
        self.__clear_line(line2)
        if metadata is None:
            self.screen.addstr(line1, 1, no_media_en)
            self.screen.addstr(line2, 1, no_progress_en)
        else:
            info_line = metadata['title'] + cfg.song_sep + metadata['artist']
            self.screen.addstr(line1, 1, info_line)
            progress_bar = self.__build_progress_str(metadata)
            self.screen.addstr(line2, 1, progress_bar)
        self.__draw_border()
        self.__set_cursor()
        self.screen.refresh()
