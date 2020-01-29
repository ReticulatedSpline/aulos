import os
from functools import partial
from pynput.keyboard import Listener, KeyCode, Key

import cfg
from view import View, Direction
from player import Player


def on_press(key: KeyCode, view: View, player: Player):
    """Callback for handling user input."""
    if hasattr(key, 'char'):
        if key.char == 'p':
            view.notify('Play')
            player.play()
        elif key.char == 'a':
            view.notify('Pause')
            player.pause()
        elif key.char == 'n':
            view.notify('Skip forward')
            player.skip_forward()
        elif key.char == 'l':
            view.notify('Skip Back')
            player.skip_back()
        elif key.char == 'q':
            view.notify('Exit')
            return False
    else:
        if key == Key.up:
            view.notify('Navigate up')
            view.navigate(Direction.UP)
        elif key == Key.down:
            view.notify('Navigate down')
            view.navigate(Direction.DOWN)
        elif key == Key.right:
            view.notify('Navigate select')
            view.navigate(Direction.SELECT)
        elif key == Key.left:
            view.notify('Navigate back')
            view.navigate(Direction.BACK)
    return True


def tick(view: View, player: Player):
    """For functions run periodically"""
    metadata = player.get_metadata()
    view.update_ui(metadata)


def main():
    view = View()
    player = Player()
    listener = Listener(on_press=partial(on_press, view=view, player=player))
    listener.start()
    while listener.running:
        tick(view, player)
    del player
    del view


if __name__ == "__main__":
    main()
