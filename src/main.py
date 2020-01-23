import os
from functools import partial
from pynput.keyboard import Listener
from pynput.keyboard import KeyCode as Key

import cfg
from view import View
from player import Player


def on_press(key: Key, view: View, player: Player):
    """Handle input"""
    key = str(key).strip('\'')
    if str(key) == 'p':
        view.notify('Playing...')
        player.play()
    elif key == 'a':
        view.notify('Paused')
        player.pause()
    elif key == 'n':
        view.notify('Skipping Forward...')
        player.skip_forward()
    elif key == 'l':
        view.notify('Skipping Back...')
        player.skip_back()
    elif key == 'q':
        view.notify('Exiting...')
        raise SystemExit


def tick(view: View, player: Player):
    """For functions run periodically"""
    metadata = player.get_metadata()
    view.update_ui(metadata)


def main():
    view = View()
    player = Player()
    listener = Listener(on_press=partial(on_press, view=view, player=player))
    try:
        listener.start()
        while True:
            tick(view, player)
    except SystemExit:
        listener.stop()
        del player
        del view


if __name__ == "__main__":
    main()
