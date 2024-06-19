import curses
from curses.textpad import rectangle, Textbox


class InputDialog:
    def __init__(self, main_window: "curses.window"):
        mid_line = curses.LINES // 2
        mid_col = curses.COLS // 2

        self.height = 1
        self.width = curses.COLS // 3

        self.begin_y = mid_line - (self.height // 2)
        self.begin_x = mid_col - (self.width // 2)

        self.end_y = self.begin_y + self.height
        self.end_x = self.begin_x + self.width

        self.window = main_window
        self.input = self.window.subwin(self.height, self.width, self.begin_y, self.begin_x)
        self.box = Textbox(self.input)

    def get(self):
        self.box.edit()

        message = self.box.gather()

        self.window.clear()

        return message.strip()

    def display(self, header):
        self.window.clear()
        self.window.border()

        self.window.addstr((curses.LINES // 2) - 3, 1, f"--- {header} --- [ ENTER ]".center(curses.COLS - 2).upper(), curses.A_BOLD)
        self.window.addstr((curses.LINES // 2) - 2, 1, "")

        rectangle(
            self.window,
            self.begin_y - 1,
            self.begin_x - 1,
            self.end_y,
            self.end_x
        )

        self.window.refresh()
