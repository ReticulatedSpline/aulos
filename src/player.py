import os
import vlc  # swiss army knife of media players
from mutagen.easyid3 import EasyID3 as ID3  # audio file metadata

music_path = '../music'
playlist_path = '../playlists'


class Player:
    def __init__(self):
        self.song_list = []
        self.song_idx = 0
        self.vlc = vlc.Instance()
        self.player = self.vlc.media_player_new()
        if (self.__scan_library()):
            self.media = self.vlc.media_new(
                self.song_list[self.song_idx])
            self.media.get_mrl()
            self.player.set_media(self.media)

    def __del__(self):
        return

    def __scan_library(self):
        for dirpath, _, files in os.walk(music_path):
            for file in files:
                filepath = os.path.join(dirpath, file)
                ext = os.path.splitext(filepath)
                if ext in {'mp3', 'flac'}:
                    self.song_list.append()
        if self.song_list:
            return True
        else:
            return False

    def __get_id3(self, key):
        metadata = ID3(self.song_list[self.song_idx])
        return str(metadata[key]).strip('[\']')

    def get_metadata(self):
        if (not self.song_list) or (self.song_idx < 0):
            return None
        else:
            return {
                "title": self.get_id3('title'),
                "artist": self.get_id3('artist'),
                "curr_time": self.player.get_length(),
                "run_time": self.player.get_time()
            }

    def skip_forward(self):
        self.song_idx += 1
        self.media = self.player.vlc.media_new(
            self.player.song_list[self.song_idx])
        self.media.get_mrl()
        self.player.set_media(self.media)
        self.player.play()

    def skip_back(self):
        self.song_idx -= 1
        self.media = self.player.vlc.media_new(
            self.player.song_list[self.song_idx])
        self.media.get_mrl()
        self.player.set_media(self.media)

    def pause(self):
        self.player.pause()

    def play(self):
        self.player.play()
