"""gobetween for view & model"""
import os
from enum import IntEnum
from functools import partial
from pynput.keyboard import Listener, KeyCode, Key

import cfg
from view import View, Display
from model import Player, Library


class Menu(IntEnum):
    """home menu options"""
    PLAYLISTS = 0
    ALBUMS = 1
    ARTISTS = 2
    GENRES = 3
    TRACKS = 4
    QUEUE = 5
    SETTINGS = 6
    EXIT = 7


class Direction(IntEnum):
    """navigational directions"""
    UP = 1
    DOWN = 2
    SELECT = 3
    BACK = 4


class TrackOptions(IntEnum):
    PLAY_NOW = 1
    PLAY_NEXT = 2
    PLAY_LAST = 3
    EDIT_TAGS = 4
    DELETE_TRACK = 5


class Controller:
    def __init__(self):
        self.view = View()
        self.library = Library()
        self.player = Player(self.library)

    def handle_song_select(self):
        display = self.view.menu_stack[-1]
        index = display.index + display.start_index
        if index == TrackOptions.PLAY_NOW:
            pass
        elif index == TrackOptions.PLAY_NEXT:
            pass
        elif index == TrackOptions.PLAY_LAST:
            pass
        elif index == TrackOptions.EDIT_TAGS:
            pass
        elif index == TrackOptions.DELETE_TRACK:
            pass

    def handle_playlist_select(self, item_path: str, display):
        with open(item_path, 'r') as playlist:
            tracks = list()
            for line in playlist:
                tracks.append(('t', line))
        new_display = Display(tracks, item_path)
        self.view.menu_stack.append(new_display)

    def handle_folder_select(self, item_path: str, display):
        item_name = item_path.split(os.sep)[-1]
        display_path = display.menu_path + cfg.sep + item_name
        item_list = self.library.get_disk_items(item_path)
        new_display = Display(item_list, display_path)
        self.view.menu_stack.append(new_display)

    def handle_home_select(self):
        display = self.view.menu_stack[-1]
        index = display.index + display.start_index
        path = cfg.sep
        if index == Menu.EXIT:
            return False
        elif index == Menu.PLAYLISTS:
            path += 'playlists'
            items = self.library.get_disk_items(cfg.playlist_dir)
            display = Display(items, path)
            self.view.menu_stack.append(display)
        elif index == Menu.TRACKS:
            path += 'tracks'
            display = Display(self.library.music, path)
            self.view.menu_stack.append(display)
        elif index == Menu.ALBUMS:
            self.view.notify("Not yet implemented!")
        elif index == Menu.ARTISTS:
            self.view.notify("Not yet implemented!")
        elif index == Menu.GENRES:
            self.view.notify("Not yet implemented!")
        elif index == Menu.QUEUE:
            self.view.notify("Not yet implemented!")
        elif index == Menu.SETTINGS:
            self.view.notify("Not yet implemented!")
        return True

    def handle_select(self):
        display = self.view.menu_stack[-1]
        item = display.get_selected_item()
        if not display.menu_path:
            return self.handle_home_select()
        elif item[0] == 'd':
            self.handle_folder_select(item[1], display)
        elif item[0] == 'p':
            self.handle_playlist_select(item[1], display)
        elif item[0] == 't':
            self.handle_song_select()

    def navigate(self, direction: Direction):
        """handle menu scrolling by manipulating display tuples"""
        display = self.view.menu_stack[-1]
        if direction is Direction.UP:
            self.view.navigate_up(display)
        elif direction is Direction.DOWN:
            self.view.navigate_down(display)
        elif direction is Direction.BACK:
            if len(self.view.menu_stack) > 1:
                self.view.menu_stack.pop()
        elif direction is Direction.SELECT:
            return self.handle_select()

    def on_press(self, key: KeyCode):
        """Callback for handling user input."""
        if hasattr(key, 'char'):
            if key.char == 'p':
                self.player.play()
            elif key.char == 'a':
                self.player.pause()
            elif key.char == 'n':
                self.player.skip_forward()
            elif key.char == 'l':
                self.player.skip_back()
            return True
        else:
            action = None
            if key == Key.up:
                return self.navigate(Direction.UP)
            elif key == Key.down:
                return self.navigate(Direction.DOWN)
            elif key == Key.right:
                return self.navigate(Direction.SELECT)
            elif key == Key.left:
                return self.navigate(Direction.BACK)

    def tick(self):
        """periodic ui update"""
        metadata = self.player.get_metadata()
        self.view.update_ui(metadata)

    def run(self):
        """splits into two threads for ui and pynput"""
        listener = Listener(on_press=self.on_press)
        listener.start()
        while listener.running:
            self.tick()
