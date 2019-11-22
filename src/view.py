import curses  # textual user interface

version = '0.0.1'
prompt = '[P]lay, P[a]use, [N]ext, [L]ast, [Q]uit ▶ '


class View:
    def __init__(self):
        self.screen = curses.initscr()
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()

        # draw border and title
        self.screen.border(0)
        title = 'OpenDAP' + ' ' + version
        self.screen.addstr(0, (self.max_x_chars - len(title)) // 2, title)

        self.screen.addstr(self.max_y_chars - 4, 1, "Nothing is playing!")
        self.screen.addstr(self.max_y_chars - 3, 1, "Cannot display progress.")
        self.screen.addstr(self.max_y_chars - 2, 1, prompt)
        self.screen.refresh()

    def __del__(self):
        print('Destroying curses windows...')
        curses.endwin()

    def update_ui(self, metadata):
        if metadata is None:
            self.screen.addstr(self.max_y_chars - 4, 1, "Nothing is playing!")
            self.screen.addstr(self.max_y_chars - 3, 1,
                               "Cannot display progress.")
        else:
            run_time = int(round(metadata["run_time"] / 1000))
            current_time = int(round(metadata["curr_time"] / 1000))
            self.screen.addstr(self.max_y_chars - 4, 1,
                               metadata['title'] + ' by ' + metadata['artist'])
        self.screen.move(self.max_y_chars - 2, len(prompt) + 2)  # +1 border, +1 space
        self.screen.refresh()
