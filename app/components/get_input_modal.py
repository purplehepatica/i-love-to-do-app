import curses
from curses.textpad import rectangle, Textbox


def get_input_modal(main_window: "curses.window"):
    mid_line = round(curses.LINES / 2)
    mid_col = round(curses.COLS / 2)

    editwin_lines = 2
    editwin_columns = round(curses.COLS / 3)

    editwin_start_y = mid_line - round(editwin_lines / 2)
    editwin_start_x = mid_col - round(editwin_columns / 2)

    editwin_end_y = mid_line + round(editwin_lines / 2)
    editwin_end_x = mid_col + round(editwin_columns / 2)

    editwin = curses.newwin(
        editwin_lines, editwin_columns, editwin_start_y, editwin_start_x
    )

    main_window.addstr(mid_line - 3, 0, "Wprowadź nazwę projektu: (CTRL + G to save)".center(curses.COLS))

    rectangle(main_window, editwin_start_y - 1, editwin_start_x - 1, editwin_end_y, editwin_end_x + 1)

    box = Textbox(editwin)

    main_window.refresh()

    box.edit()

    message = box.gather()

    main_window.clear()

    return message.strip()
