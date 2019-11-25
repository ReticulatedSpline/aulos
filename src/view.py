import cfg # settings
import curses  # textual user interface

version = '0.0.1'
prompt = '[P]lay, P[a]use, [N]ext, [L]ast, [Q]uit ▶ '
title = 'OpenDAP' + ' ' + version

class View:
    def __init__(self):
        self.screen = curses.initscr()
        self.max_y_chars, self.max_x_chars = self.screen.getmaxyx()

        # draw border and title
        self.screen.border(0)
        self.screen.addstr(0, (self.max_x_chars - len(title)) // 2, title)

        self.screen.addstr(self.max_y_chars - 4, 1, "Nothing is playing!")
        self.screen.addstr(self.max_y_chars - 3, 1, "Cannot display progress.")
        self.screen.addstr(self.max_y_chars - 2, 1, prompt)

        self.noti_timer = 0
        self.noti_length = 0

        self.screen.refresh()

    def __del__(self):
        self.notify('Destroying curses windows...')
        curses.endwin()

    def notify(self, string):
        self.screen.addstr(1, 1, string)
        self.noti_timer = 0
        self.noti_length = len(string)
        
    def update_ui(self, metadata):
        line1_loc = self.max_y_chars - 4
        line2_loc = self.max_y_chars - 3

        if self.noti_timer > cfg.noti_timeout:
            self.screen.addstr(2, 1, ' ' * self.noti_length)
            self.noti_timer = 0
        else:
            self.noti_timer += 1
        self.screen.addstr(2, 1, str(self.noti_timer) + ' of ' + str(cfg.noti_timeout))
        if metadata is None:
            self.screen.addstr(line1_loc, 1, "Nothing is playing!")
            self.screen.addstr(line2_loc, 1, "Cannot display progress.")
        else:
            run_time = int(round(metadata["run_time"] / 1000))
            current_time = int(round(metadata["curr_time"] / 1000))
            self.screen.addstr(line1_loc, 1, metadata['title'] + ' by ' + metadata['artist'])
            progress = '[' + '░' * ((run_time // current_time) * self.max_x_chars - 10) + '] ' \
                + str(current_time) + ' of ' + str(run_time)
            self.screen.addstr(line2_loc, 1, progress)
        self.screen.move(self.max_y_chars - 2, len(prompt) + 2)
        self.screen.refresh()
