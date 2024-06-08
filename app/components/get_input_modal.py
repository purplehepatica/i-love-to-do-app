import curses
from curses.textpad import rectangle, Textbox


def get_input_modal(main_window: "curses.window"):
    mid_line = round(curses.LINES / 2)
    mid_col = round(curses.COLS / 2)

    input_window_lines = 2
    input_window_columns = round(curses.COLS / 3)

    input_window_start_y = mid_line - round(input_window_lines / 2)
    input_window_start_x = mid_col - round(input_window_columns / 2)

    input_window_end_y = mid_line + round(input_window_lines / 2)
    input_window_end_x = mid_col + round(input_window_columns / 2)

    input_window = curses.newwin(
        input_window_lines, input_window_columns, input_window_start_y, input_window_start_x
    )

    main_window.addstr(mid_line - 3, 0, "Wprowadź nazwę projektu: (naciśnij CTRL + G, by zapisać)".center(curses.COLS))

    rectangle(main_window, input_window_start_y - 1, input_window_start_x - 1, input_window_end_y, input_window_end_x + 1)

    box = Textbox(input_window)

    main_window.refresh()

    box.edit()

    message = box.gather()

    main_window.clear()

    return message.strip()
