import cfg  # settings
import curses  # textual user interface
from datetime import timedelta

class View:
    """Wrap the python Curses library and handle all aspects of the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()

        self.__draw_border()

        self.screen.addstr(self.max_y_chars - 4, 1, cfg.no_load_en)
        self.screen.addstr(self.max_y_chars - 3, 1, cfg.no_load_en)
        self.screen.addstr(self.max_y_chars - 2, 1, cfg.prompt_en)

        self.screen.refresh()

    def __del__(self):
        """Restore the previous state of the terminal"""
        curses.endwin()

    def __draw_border(self):
        self.screen.border(0)
        self.screen.addstr(0, (self.max_x_chars - len(cfg.title)) // 2, cfg.title)

    def __set_cursor(self):
        self.screen.move(self.max_y_chars - 2, len(cfg.prompt_en) + 2)

    def __clear_line(self, line: int):
        self.screen.move(line, 1)
        self.screen.clrtoeol()
        self.__draw_border()

    def __strfdelta(self, tdelta: timedelta, fmt: str):
        """Taken from https://stackoverflow.com/a/8907269"""
        d = {"days": tdelta.days}
        d["hours"], rem = divmod(tdelta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

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

        run_time_str = self.__strfdelta(timedelta(seconds=run_time), cfg.time_format)
        curr_time_str = self.__strfdelta(timedelta(seconds=curr_time), cfg.time_format)
        time_str = curr_time_str + cfg.time_sep_en + run_time_str + ' (' + str(percent) + '%)'

        fill_count = int(15 * curr_time / run_time)
        progress_fill = cfg.prog_fill * fill_count
        progress_void = ' ' * (15 - fill_count)

        return '[' + progress_fill + progress_void + '] ' + time_str

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
            self.screen.addstr(line1, 1, cfg.no_media_en)
            self.screen.addstr(line2, 1, cfg.no_progress_en)
        else:
            if metadata['playing']:
                info_line = metadata['title'] + cfg.song_sep_en + metadata['artist']
            else:
                info_line = cfg.no_load_en
            self.screen.addstr(line1, 1, info_line)
            progress_bar = self.__build_progress_str(metadata)
            self.screen.addstr(line2, 1, progress_bar)
        self.__draw_border()
        self.__set_cursor()
        self.screen.refresh()
