import sys, os
from pynput import keyboard
from functools import partial

import cfg
from view import View
from player import Player

exit_signal: bool = False
def on_press(key: keyboard.KeyCode, view: View, player: Player):
    """Handle input"""
    global exit_signal
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
        exit_signal = True
        return False
    view.update_ui(player.get_metadata())


def tick(view: View, player: Player):
    """For functions run periodically"""
    metadata = player.get_metadata()
    view.update_ui(metadata)


def main():
    view = View()
    player = Player()

    view.notify("Ready!")
    with keyboard.Listener(on_press=partial(on_press, view=view, player=player)) as listener:
        while exit_signal is False:
            tick(view, player)
        del player
        del view
        listener.join() # merge to one thread
        os.system('reset') # clean up the console


if __name__ == "__main__":
    main()
