import os
import vlc  # swiss army knife of media players
from mutagen.easyid3 import EasyID3 as ID3  # audio file metadata

music_path = os.path.abspath(os.path.join(__file__, '../../music'))
playlist_path = os.path.abspath(os.path.join(__file__, '../../playlists'))


class Player:
    """Wrap calls to the VLC plugin and handle scanning for media."""

    def __init__(self):
        self.song_list = []
        self.song_idx = 0
        self.song_idx_max = 0
        self.vlc = vlc.Instance()
        self.player = self.vlc.media_player_new()
        self.__scan_library()
        self.__update_song()

    def __del__(self):
        return

    def __scan_library(self):
        for dirpath, _, files in os.walk(music_path):
            for file in files:
                filepath = os.path.join(dirpath, file)
                ext = os.path.splitext(filepath)
                if ext in {'mp3', 'flac'}:
                    self.song_list.append()
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
            return {
                "title": self.get_id3('title'),
                "artist": self.get_id3('artist'),
                "curr_time": self.player.get_length(),
                "run_time": self.player.get_time()
            }

    def play(self):
        """Start playing the current track."""
        self.player.play()

    def pause(self):
        """Pause the current track. Position is preserved."""
        self.player.pause()

    def skip_forward(self):
        """Skip the the beginning of the next song and start playing."""
        if (self.song_idx >= self.song_idx_max):
            self.song_idx = 0
        else:
            self.song_idx += 1
        self.__update_song()
        self.play()

    def skip_back(self):
        """Skip to the beginning of the last song and start playing."""
        if (self.song_idx > 0):
            self.song_idx -= 1
        self.__update_song()
        self.play()
