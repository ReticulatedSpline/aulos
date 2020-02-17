"""gobetween for view & model"""
from functools import partial
from pynput.keyboard import Listener, KeyCode, Key

from view import View, Direction, Display, Menu
from model import Library, Player


def handle_home_select(view: View, library: Library):
    display = view.menu_stack[-1]
    index = display.index + display.start_index
    if index == Menu.EXIT:
        return False
    elif index == Menu.PLAYLISTS:
        path = display.menu_path + '/playlists'
        display = Display(path, library.playlists, 0, 0)
        view.menu_stack.append(display)
    elif index == Menu.TRACKS:
        path = display.menu_path + '/tracks'
        display = Display(path, library.music, 0, 0)
        view.menu_stack.append(display)
    elif index == Menu.ALBUMS:
        view.notify("Not yet implemented!")
    elif index == Menu.ARTISTS:
        view.notify("Not yet implemented!")
    elif index == Menu.GENRES:
        view.notify("Not yet implemented!")
    elif index == Menu.QUEUE:
        view.notify("Not yet implemented!")
    elif index == Menu.SETTINGS:
        view.notify("Not yet implemented!")
    return True


def navigate(view: View, library: Library, direction: Direction):
    """handle menu scrolling by manipulating display tuples"""
    display = view.menu_stack[-1]
    if direction is Direction.UP:
        view.navigate_up(display)
    elif direction is Direction.DOWN:
        view.navigate_down(display)
    elif direction is Direction.BACK:
        if len(view.menu_stack) > 1:
            view.menu_stack.pop()
    elif direction is Direction.SELECT:
        if display.menu_path.endswith('home'):
            return handle_home_select(view, library)
        else:
            view.notify('Not yet implemented')


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
            return navigate(view, library, Direction.UP)
        elif key == Key.down:
            return navigate(view, library, Direction.DOWN)
        elif key == Key.right:
            return navigate(view, library, Direction.SELECT)
        elif key == Key.left:
            return navigate(view, library, Direction.BACK)


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
