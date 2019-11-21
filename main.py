import os
import time
import vlc  # swiss army knife of media players
import curses # textual user interface
from progress.bar import Bar
from mutagen.easyid3 import EasyID3 as ID3  # audio file metadata
from pynput.keyboard import Key, Listener # detect keypresses, deprecate after touchscreen

music_path = 'music'

class Player:
    def __init__(self):
        self.song_list = []
        self.song_idx = 0
        self.vlc = vlc.Instance()
        self.player = self.vlc.media_player_new()
        self.scan_songs()
        self.media = self.vlc.media_new(self.song_list[self.song_idx])
        self.media.get_mrl()
        self.player.set_media(self.media)

    def scan_songs(self):
        for dirpath, dirnames, files in os.walk(music_path):
            for file in files:
                self.song_list.append(os.path.join(dirpath, file))
    
    def get_id3_key(self, key):
        metadata = ID3(self.song_list[self.song_idx])
        return str(metadata[key]).strip('[\']')
    
    def get_title(self):
        return self.get_id3_key('title')

    def get_artist(self):
        return self.get_id3_key('artist')

    def get_curr_time(self):
        return self.player.get_length()
    
    def get_total_time(self):
        return self.player.get_time()

    def skip_forward(self):
        self.song_idx += 1
        self.media = player.vlc.media_new(player.song_list[self.song_idx])
        self.media.get_mrl()
        self.player.set_media(self.media)
        self.player.play()

    def skip_back(self):
        self.song_idx -= 1
        self.media = player.vlc.media_new(player.song_list[self.song_idx])
        self.media.get_mrl()
        self.player.set_media(self.media)

    def pause(self):
        self.player.pause()

    def play(self):
        self.player.play()

class View:
    def __init__(self):
        self.progress_bar = Bar('', max=0)
        self.screen = curses.initscr()

    def update_ui(self, play_time, total_time):
        total_time = int(round(play_time / 1000))
        if not total_time:
            return
        current_time = int(round(total_time / 1000))
        self.progress_bar.max = total_time
        self.progress_bar.progress = current_time / total_time


def on_press(key, player, view):
    if key == 'p':
        print("Playing...")
        player.play()
        return
    elif key == 'a':
        print("Pausing...")
        player.pause()
    elif key == 'n':
        print("Skipping...")
        player.skip_forward()
        return
    elif key == 'l':
        print("Skipping back...")
        player.skip_back()
        return
    elif key == 'q':
        print("Exiting...")
        exit(0)
        return
    view.update_ui(player.get_curr_time(), player.get_total_time())
    return

view = View()
player = Player()

key = ''
hotkeys = {ord('p'), ord('a'), ord('n'), ord('l'), ord('q')}
while True:
    key = view.screen.getch()
    if key in hotkeys:
        on_press(key, player, view)
    view.screen.clear()
    view.screen.addstr(player.get_title() + ' by ' + player.get_artist())
    # Changes go in to the screen buffer and only get
    # displayed after calling `refresh()` to update
    view.screen.refresh()

# curses.napms(5000) # sleep
curses.endwin()