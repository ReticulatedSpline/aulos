import cfg  # settings
import curses  # textual user interface

version = '0.0.0.1'
prompt = '[P]lay, P[a]use, [N]ext, [L]ast, [Q]uit ▶ '
title = 'OpenDAP' + ' ' + version
no_media_en = "Nothing is playing!"
no_progress_en = "Cannot display progress."
song_by_en = " by "

class View:
    """Wrap the python Curses library and handle all aspects of the TUI."""

    def __init__(self):
        self.screen = curses.initscr()
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()

        self.screen.border(0)
        self.screen.addstr(0, (self.max_x_chars - len(title)) // 2, title)

        self.screen.addstr(self.max_y_chars - 4, 1, no_media_en)
        self.screen.addstr(self.max_y_chars - 3, 1, no_progress_en)
        self.screen.addstr(self.max_y_chars - 2, 1, prompt)

        self.screen.refresh()

    def __del__(self):
        curses.endwin()

    def __set_cursor(self):
        self.screen.move(self.max_y_chars - 2, len(prompt) + 2)

    def __clear_line(self, line: int):
        self.screen.move(line, 1)
        self.screen.clrtoeol()
        self.screen.border(0)

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
            info_line = metadata['title'] + ' by ' + metadata['artist']
            self.screen.addstr(line1, 1, info_line)

            run_time = round(metadata["run_time"] / 1000)
            current_time = round(metadata["curr_time"] / 1000)
            if not current_time:
                self.__set_cursor()
                self.screen.refresh()
                return
            progress_fill = cfg.prog_fill * ((run_time // current_time) * self.max_x_chars - 10)
            time_str = str(current_time) + song_by_en + str(run_time)
            progress_bar = '[' + progress_fill + '] ' + time_str
            self.screen.addstr(line2, 1, progress_bar)
        self.__set_cursor()
        self.screen.refresh()
