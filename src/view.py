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
        days = tdelta.days
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        time_str = ''
        if days > 0:
            time_str += str(days) + ' days, '
        if hours > 0:
            time_str += str(hours) + ' hours '
        time_str += str(minutes)
        time_str += ':'
        if (seconds < 10):
            time_str += '0'
        time_str += str(seconds)
        return time_str

    def __update_progress_info(self, metadata):
        if metadata is None:
            return

        run_time = metadata["run_time"]
        curr_time = metadata["curr_time"]

        if run_time == 0:
            return

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
        self.__clear_line(self.line3)
        if metadata is None:
            return
        else:
            if metadata['playing']:
                info_line = metadata['title'] + cfg.song_sep_en + metadata['artist']
                self.screen.addstr(self.line1, 1, info_line)
            self.screen.addstr(2, 1, cfg.prompt_en)
            self.__update_progress_info(metadata)
        self.__draw_border()
        self.__set_cursor()
        self.screen.refresh()
