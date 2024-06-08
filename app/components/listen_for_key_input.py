import curses


# może być oczekiwanie na key_input oddzielne dla różnych okien
def listen_for_key_input(main_window: "curses.window"):
    return main_window.getch()
