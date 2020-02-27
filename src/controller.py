import os
from time import sleep
from enum import IntEnum
from functools import partial
from pynput.keyboard import Listener, KeyCode, Key

import cfg
from display import ItemType, Display, DisplayItem
from view import View
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


class MediaOptions(IntEnum):
    """options for playlists, library subsets, and single tracks"""
    PLAY = 0
    VIEW = 1
    QUEUE_NEXT = 2
    QUEUE_LAST = 3
    DELETE = 4


class Controller:
    """handle menu transitions, and act as gobetween for model/view"""
    def __init__(self):
        self.view = View()
        self.library = Library()
        self.player = Player(self.library)

    def handle_song_select(self):
        display = self.view.menu_stack[-1]
        index = display.index + display.start_index
        if index == MediaOptions.PLAY_NOW:
            pass
        elif index == MediaOptions.PLAY_NEXT:
            pass
        elif index == MediaOptions.PLAY_LAST:
            pass
        elif index == MediaOptions.EDIT_TAGS:
            pass
        elif index == MediaOptions.DELETE_TRACK:
            pass

    def handle_playlist_select_view(self, file_path: str):
        if not os.path.isfile(file_path):
            return
        with open(file_path, 'r') as playlist:
            tracks = list()
            for line in playlist:
                tracks.append(DisplayItem(ItemType.Track, line))
        new_display = Display(tracks, file_path)
        self.view.menu_stack.append(new_display)

    def handle_media_select(self, item_path: str, display):
        items = list()
        for opt in cfg.media_option_items:
            items.append(DisplayItem(ItemType.Menu, opt))
        new_display = Display(items, item_path)
        self.view.menu_stack.append(new_display)

    def handle_dir_select(self, item_path: str, display):
        item_name = item_path.split(os.sep)[-1]
        display_path = display.menu_path + os.sep + item_name
        item_list = self.library.get_disk_items(item_path)
        new_display = Display(item_list, display_path)
        self.view.menu_stack.append(new_display)

    def handle_home_select(self):
        display = self.view.menu_stack[-1]
        index = display.index + display.start_index
        if index == Menu.EXIT:
            return False
        elif index == Menu.PLAYLISTS:
            path = cfg.home_menu_items[Menu.PLAYLISTS]
            items = self.library.get_disk_items(cfg.playlist_dir)
            display = Display(items, path)
            self.view.menu_stack.append(display)
        elif index == Menu.TRACKS:
            path = cfg.home_menu_items[Menu.TRACKS]
            display = Display(self.library.get_tracks(), path)
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
        display: Display = self.view.menu_stack[-1]
        item: DisplayItem = display.get_selected_item()
        ext: str = os.path.splitext(display.menu_path)[1]
        if not display.menu_path:
            return self.handle_home_select()
        elif item.item_type is ItemType.Menu:
            if ext in cfg.playlist_formats:
                if item.path == cfg.media_option_items[MediaOptions.VIEW]:
                    self.handle_playlist_select_view(display.menu_path)
        elif item.item_type is ItemType.Directory:
            self.handle_dir_select(item.path, display)
        elif item.item_type in (ItemType.Track, ItemType.Playlist):
            self.handle_media_select(item.path, display)

    def navigate(self, direction: Direction):
        """handle menu scrolling by manipulating display tuples"""
        self.view.menu_changed = True
        if direction is Direction.UP:
            self.view.navigate_up()
        elif direction is Direction.DOWN:
            self.view.navigate_down()
        elif direction is Direction.BACK:
            self.view.navigate_back()
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
        self.view.update_status(metadata)
        if self.view.menu_changed:
            self.view.update_menu()

    def run(self):
        """splits into two threads for ui and pynput"""
        listener = Listener(on_press=self.on_press)
        listener.start()
        while listener.running:
            self.tick()
            sleep(cfg.refresh_rate)
