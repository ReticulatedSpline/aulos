"""gobetween for view & model"""

import os
from time import sleep
from functools import partial
from pynput.keyboard import Listener, KeyCode, Key

from view import View, Direction
from model import Player, Library


def on_press(key: KeyCode, view: View, player: Player):
    """Callback for handling user input."""
    if hasattr(key, 'char'):
        if key.char == 'p':
            player.play()
        elif key.char == 'a':
            player.pause()
        elif key.char == 'n':
            player.skip_forward()
        elif key.char == 'l':
            player.skip_back()
    else:
        if key == Key.up:
            view.navigate(Direction.UP)
        elif key == Key.down:
            view.navigate(Direction.DOWN)
        elif key == Key.right:
            return view.navigate(Direction.SELECT)
        elif key == Key.left:
            view.navigate(Direction.BACK)
    return True


def tick(view: View, player: Player):
    """periodic ui update"""
    metadata = player.get_metadata()
    view.update_ui(metadata)


def start():
    """splits into two threads for ui and pynput"""
    view = View()
    library = Library()
    player = Player(library)
    listener = Listener(on_press=partial(on_press, view=view, player=player))
    listener.start()
    while listener.running:
        tick(view, player)
    del view
