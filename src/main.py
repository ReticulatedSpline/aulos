import time, sys, os
from pynput import keyboard
from functools import partial

from view import View
from player import Player

exit_signal = False
def on_press(key: keyboard.KeyCode, view: View, player: Player):
    """Handle keypresses. Deprecate for touchscreen eventually."""
    global exit_signal
    key = str(key).strip('\'')
    if str(key) == 'p':
        view.notify('Playing...')
        player.play()
    elif key == 'a':
        view.notify('Pausing...')
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
        del player
        del view
        return False
    view.update_ui(player.get_metadata())


view = View()
player = Player()
with keyboard.Listener(on_press=partial(on_press, view=view, player=player)) as listener:
    while exit_signal == False:
        time.sleep(1)
    listener.join()
    os.system('reset')