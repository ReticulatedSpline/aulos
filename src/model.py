import os
import vlc
from glob import glob
from mutagen.easyid3 import EasyID3 as get_tags

from display import DisplayItem, ItemType
import cfg


class Library:
    """handle scanning and indexing media"""

    def __init__(self):
        self.music = list()
        self.last_played = list()
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


class Player:
    """track player state and wrap calls to VLC"""

    def __init__(self, library: Library):
        self.queue: list = library.music
        self.played: list = list()
        self.curr_track_path: str = self.queue[0]
        self.curr_track: MediaPlayer = vlc.MediaPlayer(self.curr_track_path)
        self.played.append(self.queue.pop())

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
        """play the passed track or track list"""

        if (len(self.queue) > 0):
            self.played.append(self.queue.pop())

        if media is list:
            self.queue.extend(media)
        elif os.path.isfile(media):
            self.queue.append(media)
        else:
            return

        self.curr_track = vlc.MediaPlayer(self.queue[0])
        return True if self.curr_track.play() >= 0 else False

    def pause(self):
        """pause the current track, preserving position"""
        if self.curr_track:
            self.curr_track.pause()

    def enqueue(items: list):
        self.queue = self.queue + items

    def skip_forward(self):
        """skip the the beginning of the next track"""
        if len(self.queue) <= 1:
            return
        song_path = self.queue.pop()
        if not os.path.isfile(song_path):
            return
        self.curr_track_path = song_path
        self.curr_track = vlc.MediaPlayer(song_path)
        played.append(song_path)
        self.play()

    def skip_back(self):
        """skip to the beginning of the last track"""
        if len(self.played) <= 1:
            return
        song_path = last.pop()
        if not os.path.isfile(song_path):
            return
        self.curr_track_path = song_path
        self.curr_track = vlc.MediaPlayer(song_path)
        self.queue.append(song_path)
        self.play()
