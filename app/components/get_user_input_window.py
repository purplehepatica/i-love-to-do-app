import curses
from curses.textpad import rectangle, Textbox


class InputModal:
    def __init__(self, main_window: "curses.window"):
        self.main_window = main_window

    def create(self):
        pass

    def show(self):
        pass

    def get(self, box):
        pass


def get_user_input_window(main_window: "curses.window"):
    # main_window.clear()

    modal_lines = curses.LINES
    modal_columns = curses.COLS

    modal_start_y = 0
    modal_start_x = 0

    modal_window = curses.newwin(
        modal_lines, modal_columns, modal_start_y, modal_start_x
    )

    modal_window.border()

    mid_line = round(curses.LINES / 2)
    mid_col = round(curses.COLS / 2)

    input_window_lines = 1
    input_window_columns = round(curses.COLS / 3)

    input_window_start_y = mid_line - round(input_window_lines / 2)
    input_window_start_x = mid_col - round(input_window_columns / 2)

    input_window_end_y = mid_line + round(input_window_lines / 2)
    input_window_end_x = mid_col + round(input_window_columns / 2)

    input_window = curses.newwin(
        input_window_lines, input_window_columns, input_window_start_y, input_window_start_x
    )

    modal_window.addstr(mid_line - 3, 0, "Wprowadź nazwę projektu: (naciśnij CTRL + G, by zapisać)".center(curses.COLS))

    rectangle(
        modal_window,
        input_window_start_y - 1,
        input_window_start_x - 1,
        input_window_end_y + 1,
        input_window_end_x + 1
    )

    box = Textbox(input_window)

    modal_window.refresh()

    box.edit()

    message = box.gather()

    return message.strip()
