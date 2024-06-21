from enum import Enum
import curses

class ProjectActions(Enum):
    OPEN = 0
    ADD = 1
    DELETE = 2
    CHANGE_NAME = 3
    CHANGE_POSITION = 4
    EXIT = 5


class ProjectTaskActions(Enum):
    ADD = 0
    DELETE = 1
    CHANGE_NAME = 2
    CHANGE_POSITION = 3
    CLOSE = 4


def listen_for_key_input(main_window: "curses.window"):
    return main_window.getch()


def confirmation(confirmation_window):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if confirmation_window.display():
                func(*args, **kwargs)

        return wrapper
    return decorator
