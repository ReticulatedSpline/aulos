import os
import vlc  # swiss army knife of media players
import cfg
from mutagen.easyid3 import EasyID3 as ID3  # audio file metadata

music_path = os.path.abspath(os.path.join(__file__, '../../music'))
playlist_path = os.path.abspath(os.path.join(__file__, '../../playlists'))


class Player:
    """Track player state, wrap calls to the VLC plugin, and handle scanning for media."""

    def __init__(self):
        self.song_list = []
        self.song_idx = 0
        self.song_idx_max = 0
        self.vlc = vlc.Instance()
        self.__scan_library()
        self.player = self.vlc.media_player_new(self.song_list[self.song_idx])
        self.__update_song()

    def __del__(self):
        del self.vlc
        return

    def __scan_library(self):
        for dirpath, _, files in os.walk(music_path):
            for file in files:
                filepath = os.path.join(dirpath, file)
                _, ext = os.path.splitext(filepath)
                if ext in cfg.file_types:
                    self.song_list.append(filepath)
                    self.song_idx_max += 1

    def __get_id3(self, key: str):
        metadata = ID3(self.song_list[self.song_idx])
        return str(metadata[key]).strip('[\']')

    def __update_song(self):
        if self.song_list and self.song_idx < len(self.song_list):
            self.media = self.vlc.media_new(self.song_list[self.song_idx])
            self.media.get_mrl()
            self.player.set_media(self.media)

    def get_metadata(self):
        """Return a dictionary of title, artist, current runtime and total runtime."""
        if (not self.song_list) or (self.song_idx < 0):
            return None
        else:
            # default states when not playing a track are negative integers
            curr_time = self.player.get_position() * 100
            if (curr_time < 0):
                curr_time = 0
            run_time = self.player.get_length() // 1000
            if (run_time < 0):
                run_time = 0
                playing = False
            else:
                playing = True
            info = {"playing": playing,
                    "title": self.__get_id3('title'),
                    "artist": self.__get_id3('artist'),
                    "curr_time": curr_time,
                    "run_time": run_time}
            return info

    def play(self):
        """Start playing the current track."""
        self.player.play()

    def pause(self):
        """Pause the current track. Position is preserved."""
        self.player.pause()

    def skip_forward(self):
        """Skip the the beginning of the next track and start playing."""
        if (self.song_idx < self.song_idx_max):
            self.song_idx += 1
        self.__update_song()
        self.play()

    def skip_back(self):
        """Skip to the beginning of the last track and start playing."""
        if (self.song_idx > 0):
            self.song_idx -= 1
        self.__update_song()
        self.play()
