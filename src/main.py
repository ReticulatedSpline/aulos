import time, sys, os, threading
from pynput import keyboard
from functools import partial

import cfg
from view import View
from player import Player

exit_signal: bool = False
def on_press(key: keyboard.KeyCode, view: View, player: Player):
    """Handle keypresses. Deprecate for touchscreen eventually."""
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
        del player
        del view
        return False
    view.update_ui(player.get_metadata())

def tick(view: View, player:Player):
    """Periodic UI update. This would be better suited as a class method, but I'm unsure how to
    do that without making the player and view classes cross-dependent. Could be part
    of controller if refactored into an MVC architecture."""
    metadata = player.get_metadata()
    view.update_ui(metadata)

view = View()
player = Player()

view.notify("Ready!")
with keyboard.Listener(on_press=partial(on_press, view=view, player=player)) as listener:
    while exit_signal == False:
        tick(view, player)
    listener.join() # merge to one thread
    os.system('reset') # clean up the console