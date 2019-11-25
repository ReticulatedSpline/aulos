import time
from pynput import keyboard
from functools import partial

from view import View
from player import Player


def on_press(key, view, player):
    view.notify('Entered listener!')
    if key == ord('p'):
        view.notify('Playing...')
        player.play()
        return
    elif key == ord('a'):
        view.notify('Pausing...')
        player.pause()
    elif key == ord('n'):
        view.notify('Skipping forward...')
        player.skip_forward()
        return
    elif key == ord('l'):
        view.notify('Skipping back...')
        player.skip_back()
        return
    elif key == ord('q'):
        view.notify('Quitting...')
        del view
        del player
        exit(0)
    view.update_ui(player.get_metadata())

view = View()
player = Player()
listener = keyboard.Listener(
    on_press=partial(on_press, view=view, player=player))
listener.start()

while True:
    view.update_ui(player.get_metadata())
    continue