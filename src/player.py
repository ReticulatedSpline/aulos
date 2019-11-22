import os
import vlc  # swiss army knife of media players
from mutagen.easyid3 import EasyID3 as ID3  # audio file metadata

music_path = '../music'
playlist_path = '../playlists'


class Player:
    def __init__(self):
        self.__song_list = []
        self.__song_idx = 0
        self.__vlc = vlc.Instance()
        self.__player = self.__vlc.media_player_new()
        if (self.__scan_library()):
            self.__media = self.__vlc.media_new(
                self.__song_list[self.__song_idx])
            self.__media.get_mrl()
            self.__player.set_media(self.__media)

    def __del__(self):
        print('Destroying VLC module...')

    def __scan_library(self):
        for dirpath, dirnames, files in os.walk(music_path):
            for file in files:
                filepath = os.path.join(dirpath, file)
                ext = os.path.splitext(filepath)
                if ext in {'mp3', 'flac'}:
                    self.__song_list.append()
        if self.__song_list:
            return True
        else:
            return False

    def __get_id3(self, key):
        metadata = ID3(self.__song_list[self.__song_idx])
        return str(metadata[key]).strip('[\']')

    def get_metadata(self):
        if (not self.__song_list) or (self.__song_idx < 0):
            return None
        else:
            return {
                "title": self.__get_id3('title'),
                "artist": self.__get_id3('artist'),
                "curr_time": self.__player.get_length(),
                "run_time": self.__player.get_time()
            }

    def skip_forward(self):
        self.__song_idx += 1
        self.__media = self.__player.vlc.media_new(
            self.__player.song_list[self.__song_idx])
        self.__media.get_mrl()
        self.__player.set_media(self.__media)
        self.__player.play()

    def skip_back(self):
        self.__song_idx -= 1
        self.__media = self.__player.vlc.media_new(
            self.__player.song_list[self.__song_idx])
        self.__media.get_mrl()
        self.__player.set_media(self.__media)

    def pause(self):
        self.__player.pause()

    def play(self):
        self.__player.play()
