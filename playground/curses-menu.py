import curses


def main(stdscr: "curses.window") -> None:
    choice = 0

    while True:
        stdscr.clear()

        curses.curs_set(0)
        stdscr.keypad(True)
        curses.noecho()

        menu_choices = [
            "1. Wyświetl tekst 'Hello'",
            "2. Wyświetl tekst 'World!'",
            "3. Wyjdź"
        ]
        stdscr.addstr("Dokonaj wyboru:\n")

        for i, menu_choice in enumerate(menu_choices):
            if i == choice:
                stdscr.addstr(i + 1, 0, menu_choice, curses.A_UNDERLINE and curses.A_REVERSE)
            else:
                stdscr.addstr(i + 1, 0, menu_choice)

        c = stdscr.getch()

        if c == curses.KEY_UP and choice > 0:
            choice -= 1
            stdscr.refresh()
        elif c == curses.KEY_DOWN and choice < 2:
            choice += 1
            stdscr.refresh()

        if c in [curses.KEY_ENTER, 10, 13] :

            match choice:
                case 0:
                    stdscr.addstr(5, 0, "Hello")
                    stdscr.refresh()
                case 1:
                    pass
                case 2:
                    break


if __name__ == "__main__":
    curses.wrapper(main)
