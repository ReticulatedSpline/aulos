import os
import vlc
from glob import glob
from collections import deque, defaultdict
from mutagen.easyid3 import EasyID3 as get_tags

from display import DisplayItem, ItemType
import cfg


class Library:
    """handle media. uses deques for fast manipulation from both sides"""

    def __init__(self):
        self.tracks = deque()
        self.last_played = deque()
        for ext in cfg.music_formats:
            file = os.path.join(cfg.music_dir, '*' + ext)
            self.tracks.extend(glob(file))
        # TODO: should these all be in a single dict for easier display work?
        self.artists: dict = self.get_metadata_dict('artist')
        self.albums: dict = self.get_metadata_dict('album')
        self.years: dict = self.get_metadata_dict('year')
        self.genres: dict = self.get_metadata_dict('genre')

    def get_metadata_dict(self, key: str) -> dict:
        results = defaultdict(list)
        for track in self.tracks:
            metadata = get_tags(track)
            tag_list = metadata.get(key)
            if not tag_list:
                continue
            for tag in tag_list:
                results[tag].append(track)
        return results

    def get_tracks(self) -> list:
        return [DisplayItem(ItemType.Track, path) for path in self.tracks]

    def get_disk_items(self, root: str) -> list:
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
        """given a valid playlist path, return contained track paths as list"""
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

    def __del__(self):
        self.stop()

    def get_metadata(self) -> dict:
        """return a dictionary of current track's metadata"""
        if self.curr_track is None:
            return None

        metadata = get_tags(self.curr_track_path)
        if not metadata:
            return None

        run_time = self.curr_track.get_length()
        run_time = 0 if run_time < 0 else run_time / 1000   # millisec to sec
        curr_time = self.curr_track.get_time() / 1000       # millisec to sec
        if curr_time < 0:
            curr_time = 0
        return {'playing': self.curr_track.is_playing(),
                'title': metadata.get('title'),
                'artist': metadata.get('artist'),
                'album': metadata.get('album'),
                'curr_time': curr_time,
                'run_time': run_time}

    def restart_track(self):
        self.curr_track.stop()
        self.curr_track = vlc.MediaPlayer(self.curr_track_path)
        self.play()

    def play_current_track(self) -> bool:
        if self.curr_track is None:
            return False
        elif self.curr_track.is_playing() == 1:
            return True
        elif self.curr_track.play() >= 0:
            return True
        return False

    def play_next_track(self) -> bool:
        if len(self.next_tracks) <= 0:
            return False
        self.stop()
        up_next = self.next_tracks.popleft()
        self.last_tracks.appendleft(up_next)
        self.curr_track = vlc.MediaPlayer(up_next)
        self.curr_track_path = up_next
        return self.curr_track.play() >= 0

    def play(self, media=None) -> bool:
        """resume playback, or play the passed media file"""

        if media is None:
            return self.play_current_track()

        if media == self.curr_track_path:
            return True

        if not os.path.isfile(media):
            return False

        track_list: list
        media_ext = os.path.splitext(media)[1]
        if media_ext in cfg.playlist_formats:
            track_list = self.library.get_playlist_tracks(media)
        elif media_ext in cfg.music_formats:
            track_list = [media]
        else:
            return False

        self.next_tracks.clear()
        self.next_tracks.extend(track_list)
        return self.play_next_track()

    def pause(self):
        """pause the current track, preserving position"""
        if self.curr_track:
            self.curr_track.pause()

    def stop(self):
        if self.curr_track:
            self.curr_track.stop()

    def play_next(self, item: str):
        if item is None:
            return
        if item is list:
            self.next_tracks.extendleft(item)
        else:
            self.next_tracks.appendleft(item)

    def play_last(self, item: str):
        if item is None:
            return
        if item is list:
            self.next_tracks.extend(item)
        else:
            self.next_tracks.append(item)

    def skip_forward(self):
        """skip the the beginning of the next track"""
        if len(self.next_tracks) <= 0:
            return
        self.stop()

        track_path = self.next_tracks.popleft()
        if not os.path.isfile(track_path):
            return
        self.curr_track_path = track_path
        self.curr_track = vlc.MediaPlayer(track_path)
        self.last_tracks.appendleft(track_path)
        self.play()

    def skip_back(self):
        """skip to the beginning of the last track"""
        metadata = self.get_metadata()
        if metadata:
            if metadata['run_time'] <= cfg.skip_back_threshold:
                self.restart_track()
                return

        if len(self.last_tracks) <= 1:
            return

        self.stop()
        track_path = self.last_tracks.popleft()
        if not os.path.isfile(track_path):
            return
        self.curr_track_path = track_path
        self.curr_track = vlc.MediaPlayer(track_path)
        self.next_tracks.appendleft(track_path)
        self.play()
