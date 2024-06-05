import curses
from curses.textpad import Textbox, rectangle


def display_input_dialog(stdscr: "curses.window"):
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

    box = Textbox(editwin)
    box.edit()

    message = box.gather()

    stdscr.clear()

    stdscr.addstr(1, 1, message)
    stdscr.getch()


def main(stdscr: "curses.window") -> None:
    while True:
        stdscr.addstr(f"Dokonaj wyboru (i - wprowadź tekst, q - wyjdź): ".center((curses.COLS - 1)), curses.A_BOLD)

        c = stdscr.getch()

        if c == ord("i"):
            stdscr.clear()
            stdscr.refresh()
            display_input_dialog(stdscr)
        elif c == ord("q"):
            break

        stdscr.clear()


if __name__ == "__main__":
    curses.wrapper(main)
