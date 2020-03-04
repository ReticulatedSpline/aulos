import os
import vlc
from glob import glob
from collections import deque
from mutagen.easyid3 import EasyID3 as get_tags

from display import DisplayItem, ItemType
import cfg


class Library:
    """handle scanning and indexing media"""

    def __init__(self):
        self.music = deque()
        self.last_played = deque()
        for ext in cfg.music_formats:
            file = os.path.join(cfg.music_dir, '*' + ext)
            self.music.extend(glob(file))

    def get_tracks(self):
        return [DisplayItem(ItemType.Track, path) for path in self.music]

    def get_disk_items(self, root: str):
        """return a tuple list of items, their paths, & their type"""
        items = list()

        for item in os.listdir(root):
            abs_path = os.path.join(root, item)
            ext = os.path.splitext(abs_path)[-1]
            if os.path.isdir(abs_path):
                items.append(DisplayItem(ItemType.Directory, abs_path))
            elif not ext:
                continue
            elif ext in cfg.music_formats:
                items.append(DisplayItem(ItemType.Track, abs_path))
            elif ext in cfg.playlist_formats:
                items.append(DisplayItem(ItemType.Playlist, abs_path))
        return items

    @staticmethod
    def get_playlist_tracks(playlist_path: str) -> list:
        """given a valid playlist path, return the list of track paths inside it"""
        tracks = list()
        with open(playlist_path, 'r') as playlist:
            for line in playlist:
                tracks.append(line.rstrip())
        return tracks


class Player:
    """track player state and wrap calls to VLC"""

    def __init__(self, library: Library):
        self.next_tracks = deque()
        self.last_tracks = deque()
        self.library = library
        self.curr_track: MediaPlayer = None
        self.curr_track_path: str = None

    def get_metadata(self):
        """return a dictionary of current song's metadata"""
        if not self.curr_track:
            return None
        metadata = get_tags(self.curr_track_path)
        if not metadata:
            return
        curr_time = self.curr_track.get_time() / 1000   # time returned in ms
        if curr_time < 0:
            curr_time = 0
        run_time = self.curr_track.get_length()  # -1 indicates no media
        run_time = 0 if run_time < 0 else run_time / 1000  # millisec to sec
        playing = True if self.curr_track.is_playing() else False
        return {"playing": playing,
                "title": metadata['title'],
                "artist": metadata['artist'],
                "album": metadata['album'],
                "curr_time": curr_time,
                "run_time": run_time}

    def play(self, media=None):
        """resume playback, or play the passed media"""

        if media is None:
            if self.curr_track is not None:
              return True if self.curr_track.play() >= 0 else False
            return False

        track_list: list
        media_ext = os.path.splitext(media)[1]
        if os.path.isfile(media) and media_ext in cfg.playlist_formats:
            track_list = self.library.get_playlist_tracks(media)
        elif os.path.isfile(media) and media_ext in cfg.music_formats:
            track_list = list(media)
        else:
            return False

        self.next_tracks.clear()
        self.next_tracks.extend(track_list)
        up_next = self.next_tracks.popleft()
        self.last_tracks.appendleft(up_next)
        self.curr_track = vlc.MediaPlayer(up_next)
        self.curr_track_path = up_next
        return True if self.curr_track.play() >= 0 else False

    def pause(self):
        """pause the current track, preserving position"""
        if self.curr_track:
            self.curr_track.pause()

    def enqueue(self, items: list):
        self.next_tracks = self.next_tracks.extend(items)

    def skip_forward(self):
        """skip the the beginning of the next track"""
        if len(self.next_tracks) <= 1:
            return
        song_path = self.next_tracks.popleft()
        if not os.path.isfile(song_path):
            return
        self.curr_track_path = song_path
        self.curr_track = vlc.MediaPlayer(song_path)
        self.last_tracks.appendleft(song_path)
        self.play()

    def skip_back(self):
        """skip to the beginning of the last track"""
        if len(self.last_tracks) <= 1:
            return
        song_path = self.last_tracks.popleft()
        if not os.path.isfile(song_path):
            return
        self.curr_track_path = song_path
        self.curr_track = vlc.MediaPlayer(song_path)
        self.next_tracks.appendleft(song_path)
        self.play()
