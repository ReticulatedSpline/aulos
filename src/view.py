import cfg  # settings
import curses  # textual user interface
from datetime import timedelta

class View:
    """Wrap the python Curses library and handle all aspects of the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()

        self.__draw_border()

        self.line1 = self.max_y_chars - 4
        self.line2 = self.max_y_chars - 3
        self.line3 = self.max_y_chars - 2
        self.screen.refresh()

    def __del__(self):
        """Restore the previous state of the terminal"""
        curses.endwin()

    def __draw_border(self):
        self.screen.border(0)
        self.screen.addstr(0, (self.max_x_chars - len(cfg.title)) // 2, cfg.title)

    def __set_cursor(self):
        self.screen.move(2, len(cfg.prompt_en) + 2)

    def __clear_line(self, line: int):
        self.screen.move(line, 1)
        self.screen.clrtoeol()
        self.__draw_border()

    def __strfdelta(self, tdelta: timedelta):
        """Format a timedelta into a string"""
        time = {"days": tdelta.days}
        time["hours"], rem = divmod(tdelta.seconds, 3600)
        time["minutes"], time["seconds"] = divmod(rem, 60)
        if time["days"] > 0:
            time_format = cfg.time_format_dh
        elif time["hours"] > 0:
            time_format = cfg.time_format_h
        else:
            time_format = cfg.time_format
        return time_format.format(**time)

    def __build_progress_str(self, metadata):
        if metadata is None:
            return cfg.no_load_en
        run_time = metadata["run_time"]
        curr_time = metadata["curr_time"]

        if (None in [curr_time, run_time]) or (run_time <= 0):
            return cfg.no_load_en

        if run_time == 0:
            percent = 0
        else:
             percent = int((curr_time / run_time) * 100)

        run_time_str = self.__strfdelta(timedelta(seconds=run_time))
        curr_time_str = self.__strfdelta(timedelta(seconds=curr_time))

        time_str = curr_time_str + cfg.time_sep_en + run_time_str + ' (' + str(percent) + '%)'

        # two border characters
        progress_bar_chars = self.max_x_chars - 2
        fill_count = int(progress_bar_chars * curr_time / run_time)
        progress_fill = cfg.prog_fill * fill_count
        progress_void = ' ' * (progress_bar_chars - fill_count)
        progress_bar = progress_fill + progress_void

        self.screen.addstr(self.line2, 1, time_str)
        self.screen.addstr(self.line3, 1, progress_bar)

    def notify(self, string: str):
        """Add a string to the top of the window."""
        self.__clear_line(1)
        self.screen.addstr(1, 1, string)
        self.__set_cursor()
        self.screen.refresh()

    def update_ui(self, metadata: dict):
        """Update track metadata and progress indicators."""

        self.__clear_line(self.line1)
        self.__clear_line(self.line2)
        if metadata is None:
            self.screen.addstr(self.line1, 1, cfg.no_media_en)
            self.screen.addstr(self.line2, 1, cfg.no_progress_en)
        else:
            if metadata['playing']:
                info_line = metadata['title'] + cfg.song_sep_en + metadata['artist']
            else:
                info_line = cfg.no_load_en
            self.screen.addstr(self.line1, 1, info_line)
            self.screen.addstr(2, 1, cfg.prompt_en)
            self.__build_progress_str(metadata)
        self.__draw_border()
        self.__set_cursor()
        self.screen.refresh()
