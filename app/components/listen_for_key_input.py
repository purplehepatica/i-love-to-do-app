import curses


def listen_for_key_input(main_window: "curses.window"):
    return main_window.getch()
