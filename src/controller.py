"""gobetween for view & model"""
from functools import partial
from pynput.keyboard import Listener, KeyCode, Key

from view import View, Action, Direction
from model import Library, Player


def handle_action(action: Action, player: Player):
    if not action:
        return
    if action.action is ActionType.PLAY:
        player.play(action.index)


def on_press(key: KeyCode, view: View, player: Player, library: Library):
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
        return True
    else:
        action = None
        if key == Key.up:
            action = view.navigate(Direction.UP)
        elif key == Key.down:
            action = view.navigate(Direction.DOWN)
        elif key == Key.right:
            action = view.navigate(Direction.SELECT)
        elif key == Key.left:
            action = view.navigate(Direction.BACK)
        handle_action(action, player)


def tick(view: View, player: Player):
    """periodic ui update"""
    metadata = player.get_metadata()
    view.update_ui(metadata)


def start():
    """splits into two threads for ui and pynput"""
    view = View()
    library = Library()
    player = Player(library)
    listener = Listener(on_press=partial(
        on_press, view=view, player=player, library=library))
    listener.start()
    while listener.running:
        tick(view, player)
    del view
