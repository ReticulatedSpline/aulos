from typing import NamedTuple, List
from enum import IntEnum


class ItemType(IntEnum):
    """home menu options"""
    Menu = 0
    Directory = 1
    Playlist = 2
    Track = 3


class DisplayItem(NamedTuple):
    item_type: ItemType
    path: str


class Display(NamedTuple):
    """hold all information necessary to draw a display"""
    items: List[DisplayItem]
    menu_path: str = ''
    index: int = 0
    start_index: int = 0

    def get_selected_item(self):
        return self.items[self.index + self.start_index]
