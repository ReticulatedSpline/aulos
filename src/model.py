import os
import vlc
import cfg
from glob import glob
from typing import NamedTuple
from mutagen.easyid3 import EasyID3 as ID3


class MediaItem(NamedTuple):
    index: int
    path: str


class Library:
    """Handle scanning for media and manage the database"""
    def __init__(self):
        self.playlists = glob(os.path.realpath(cfg.playlist_dir) + '/*.m3u')
        self.music = list()
        for ext in cfg.file_types:
            file = os.path.join(cfg.music_dir, ext)
            self.music.extend(glob(file))

    def get_all_tracks(self):
        return self.music


class Player:
    """Track player state, wrap calls to VLC, and handle scanning for media."""

    def __init__(self, library: Library):
        self.queue = library.get_all_tracks()
        self.vlc = vlc.Instance()
        self.player = self.vlc.media_player_new(self.queue[0])
        self._update_song()

    def _get_id3(self, key: str):
        metadata = ID3(self.queue[0])
        return str(metadata[key]).strip('[\']')

    def _update_song(self):
        if self.queue:
            self.media = self.vlc.media_new(self.queue[0])
            self.media.get_mrl()
            self.player.set_media(self.media)

    def get_metadata(self):
        """Return a dictionary of title, artist, current/total runtimes."""
        if not self.queue:
            return None
        else:

            # default states when not playing a track are negative integers
            curr_time = self.player.get_time() / 1000   # time returned in ms
            if curr_time < 0:
                curr_time = 0
            run_time = self.player.get_length() / 1000
            if run_time < 0:
                run_time = 0
                playing = False
            else:
                playing = True
            info = {"playing": playing,
                    "title": self._get_id3('title'),
                    "artist": self._get_id3('artist'),
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
        # TODO

    def skip_back(self):
        """Skip to the beginning of the last track and start playing."""
        # TODO
