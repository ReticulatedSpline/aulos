import os
from time import sleep
from enum import IntEnum
from pynput.keyboard import Listener, KeyCode, Key

import cfg
from display import ItemType, Display, DisplayItem
from view import View
from model import Player, Library


class HomeOptions(IntEnum):
    """home menu options"""
    PLAYLISTS = 0
    ALBUMS = 1
    ARTISTS = 2
    GENRES = 3
    TRACKS = 4
    QUEUE = 5
    SETTINGS = 6
    EXIT = 7


class MediaOptions(IntEnum):
    """menu options for playlists and tracks"""
    PLAY = 0
    VIEW = 1
    QUEUE_NEXT = 2
    QUEUE_LAST = 3
    DELETE = 4


class Direction(IntEnum):
    """navigational directions"""
    UP = 1
    DOWN = 2
    SELECT = 3
    BACK = 4


class Controller:
    """handle menu transitions, and act as gobetween for model/view"""

    def __init__(self):
        self.view = View()
        self.library = Library()
        self.player = Player(self.library)

    def handle_track_select(self):
        display = self.view.menu_stack[-1]
        selected_item = display.get_selected_item()
        path = selected_item.path
        if path == cfg.media_option_items[MediaOptions.PLAY]:
            self.player.play(display.menu_path)
            self.view.menu_stack.pop()
            self.view.notify(cfg.playing_str)
        elif path == cfg.media_option_items[MediaOptions.QUEUE_NEXT]:
            self.player.play_next(display.menu_path)
            self.view.menu_stack.pop()
            self.view.notify(cfg.play_next_str)
        elif path == cfg.media_option_items[MediaOptions.QUEUE_LAST]:
            self.player.play_last(display.menu_path)
            self.view.menu_stack.pop()
            self.view.notify(cfg.play_last_str)
        elif path == cfg.media_option_items[MediaOptions.DELETE]:
            self.view.menu_stack.pop()
            self.view.notify(cfg.not_implemented_str)

    def handle_playlist_select_view(self, file_path: str):
        if not os.path.isfile(file_path):
            return
        with open(file_path, 'r') as playlist:
            tracks = list()
            for line in playlist:
                tracks.append(DisplayItem(ItemType.Track, line.rstrip()))
        new_display = Display(tracks, file_path)
        self.view.menu_stack.append(new_display)

    def handle_media_select(self, item_path: str, display: Display):
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

    def handle_queue_select(self):
        display_path = cfg.home_menu_items[HomeOptions.QUEUE]
        display_items = list()
        for item in self.player.next_tracks:
            display_items.append(DisplayItem(ItemType.Track, item))
        new_display = Display(display_items, display_path)
        self.view.menu_stack.append(new_display)

    def handle_home_select(self):
        display = self.view.menu_stack[-1]
        index = display.index + display.start_index
        if index == HomeOptions.EXIT:
            return False
        elif index == HomeOptions.PLAYLISTS:
            path = cfg.home_menu_items[HomeOptions.PLAYLISTS]
            items = self.library.get_disk_items(cfg.playlist_dir)
            display = Display(items, path)
            self.view.menu_stack.append(display)
        elif index == HomeOptions.TRACKS:
            path = cfg.home_menu_items[HomeOptions.TRACKS]
            display = Display(self.library.get_tracks(), path)
            self.view.menu_stack.append(display)
        elif index == HomeOptions.ALBUMS:
            self.view.notify(cfg.not_implemented_str)
        elif index == HomeOptions.ARTISTS:
            self.view.notify(cfg.not_implemented_str)
        elif index == HomeOptions.GENRES:
            self.view.notify(cfg.not_implemented_str)
        elif index == HomeOptions.QUEUE:
            self.handle_queue_select()
        elif index == HomeOptions.SETTINGS:
            self.view.notify(cfg.not_implemented_str)
        return True

    def handle_playlist_select(self, item, ext, display):
        if item.path == cfg.media_option_items[MediaOptions.VIEW]:
            self.handle_playlist_select_view(display.menu_path)
        if item.path == cfg.media_option_items[MediaOptions.PLAY]:
            if not self.player.play(display.menu_path):
                self.view.notify(cfg.play_error_str)
            else:
                self.view.notify(cfg.playing_str)
            self.view.menu_stack.pop()

    def handle_menu_select(self, item, ext, display):
        if ext in cfg.playlist_formats:
            self.handle_playlist_select(item, ext, display)
        if ext in cfg.music_formats:
            self.handle_track_select()

    def handle_select(self):
        display: Display = self.view.menu_stack[-1]
        item: DisplayItem = display.get_selected_item()
        ext: str = os.path.splitext(display.menu_path)[1]
        if not display.menu_path:
            return self.handle_home_select()
        elif item.item_type is ItemType.Menu:
            self.handle_menu_select(item, ext, display)
        elif item.item_type is ItemType.Directory:
            self.handle_dir_select(item.path, display)
        elif item.item_type in (ItemType.Track, ItemType.Playlist):
            self.handle_media_select(item.path, display)

    def on_press(self, key: KeyCode):
        """Callback for handling user input."""
        if hasattr(key, 'char'):
            if key.char == 'p':
                self.player.play()
                self.view.notify(cfg.playing_str)
            elif key.char == 'a':
                self.player.pause()
                self.view.notify(cfg.paused_str)
            elif key.char == 'n':
                self.player.skip_forward()
            elif key.char == 'l':
                self.player.skip_back()
            return True
        else:
            if key == Key.up:
                self.view.navigate_up()
            elif key == Key.down:
                self.view.navigate_down()
            elif key == Key.right:
                return self.handle_select()
            elif key == Key.left:
                self.view.navigate_back()

    def tick(self):
        """periodic ui update"""
        metadata = self.player.get_metadata()
        self.view.update_status(metadata)
        self.view.update_menu()
        self.view.screen.refresh()

    def run(self):
        """splits into two threads for ui and pynput"""
        listener = Listener(on_press=self.on_press)
        try:
            listener.start()
            while listener.running:
                self.tick()
                sleep(cfg.refresh_rate)
        finally:
            del self.view
            del self.player
            del self.library
