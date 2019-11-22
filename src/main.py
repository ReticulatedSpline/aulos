import time
from pynput import keyboard

from view import View
from player import Player


def on_press(key, player, view):
    if key == ord('p'):
        print("Playing...")
        player.play()
        return
    elif key == ord('a'):
        print("Pausing...")
        player.pause()
    elif key == ord('n'):
        print("Skipping...")
        player.skip_forward()
        return
    elif key == ord('l'):
        print("Skipping back...")
        player.skip_back()
        return
    elif key == ord('q'):
        print("Exiting...")
        del view
        del player
        exit(0)
        return
    view.update_ui(player.get_metadata())


view = View()
player = Player()

listener = keyboard.Listener(on_press=on_press)
listener.start()
while True:
    view.update_ui(player.get_metadata())
    key = view.screen.getch()
