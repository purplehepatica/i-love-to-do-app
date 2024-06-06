import curses
from curses.textpad import Textbox, rectangle

"""
1. Rozmontować obecne działanie funkcji main na pomniejsze funkcje, np.
- display_menu()
- listen_for_keyboard_input()
- execute_user_choice()

- show_modal()
- get_user_choice()

- refresh_element() / refresh_screen()
"""

def get_input_modal(stdscr: "curses.window"):
    mid_line = round(curses.LINES / 2)
    mid_col = round(curses.COLS / 2)

    editwin_lines = 4
    editwin_columns = round(curses.COLS / 3)

    editwin_start_y = mid_line - round(editwin_lines / 2)
    editwin_start_x = mid_col - round(editwin_columns / 2)

    editwin_end_y = mid_line + round(editwin_lines / 2)
    editwin_end_x = mid_col + round(editwin_columns / 2)

    editwin = curses.newwin(
        editwin_lines, editwin_columns, editwin_start_y, editwin_start_x
    )

    rectangle(stdscr, editwin_start_y - 1, editwin_start_x - 1, editwin_end_y, editwin_end_x + 1)

    # editwin.addstr("HELLO!".center(editwin_columns))

    box = Textbox(editwin)

    stdscr.refresh()

    box.edit()

    message = box.gather()

    stdscr.clear()

    return message


def menu():
    pass


def main(stdscr: "curses.window") -> None:
    choice = 0
    projects = []

    # menu & user choice (arrow up & down + ENTER)
    while True:
        stdscr.refresh()

        curses.curs_set(0)
        stdscr.keypad(True)
        curses.noecho()


        for i, project_name in enumerate(projects):
            stdscr.addstr(i + 1, 1, f"{i + 1}. {project_name}")



        mid_line = round(curses.LINES / 2)
        mid_col = round(curses.COLS / 2)

        menu_lines = 8
        menu_columns = round(curses.COLS / 3)

        menu_start_y = mid_line - round(menu_lines / 2)
        menu_start_x = mid_col - round(menu_columns / 2)

        menu_window = curses.newwin(
            menu_lines, menu_columns, menu_start_y, menu_start_x
        )

        menu_window.border()

        menu_choices = [
            "1. Dodaj projekt",
            "2. Usuń projekt",
            "3. Zapisz dane",
            "4. Wyjdź"
        ]

        menu_window.addstr(1, 1, "Co chcesz wykonać?:".center(menu_columns - 2))
        menu_window.addstr(2, 1, "-" * (menu_columns - 2))

        for i, menu_choice in enumerate(menu_choices):
            if i == choice:
                menu_window.addstr(i + 3, 1, menu_choice, curses.A_UNDERLINE and curses.A_REVERSE)
            else:
                menu_window.addstr(i + 3, 1, menu_choice)

        menu_window.refresh()
        stdscr.refresh()

        c = stdscr.getch()

        if c == curses.KEY_UP and choice > 0:
            choice -= 1
            stdscr.refresh()
        elif c == curses.KEY_DOWN and choice < 3:
            choice += 1
            stdscr.refresh()

        if c in [curses.KEY_ENTER, 10, 13]:

            match choice:
                case 0:
                    stdscr.clear()
                    project_name = get_input_modal(stdscr)

                    projects.append(project_name)
                case 1:
                    pass
                case 2:
                    break
                case 3:
                    quit()


if __name__ == "__main__":
    curses.wrapper(main)
