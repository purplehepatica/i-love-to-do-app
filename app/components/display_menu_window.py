import curses


def display_menu_window(main_window: "curses.window", choice):
    main_window.refresh()

    menu_lines = 6
    menu_columns = curses.COLS

    menu_start_y = curses.LINES - menu_lines
    menu_start_x = 0

    menu_window = curses.newwin(
        menu_lines, menu_columns, menu_start_y, menu_start_x
    )

    menu_window.border()

    menu_choices = [
        "1. Dodaj projekt",
        "2. Usuń projekt",
        "3. Otwórz projekt",
        "4. Zmień pozycję",
        "5. Wyjdź"
    ]

    menu_window.addstr(1, 1, "Co chcesz wykonać?: ".center(menu_columns - 2))
    menu_window.addstr(2, 1, "-" * (menu_columns - 2))
    menu_window.addstr(3, 1, "")

    for i, menu_choice in enumerate(menu_choices):
        attribute = curses.A_REVERSE if i == choice else curses.A_NORMAL

        menu_window.addstr(f"{menu_choice}   ", attribute)

    menu_window.refresh()
