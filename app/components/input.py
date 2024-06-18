import curses
from curses.textpad import rectangle, Textbox


class NotMineTextboxWithUtfSupport(Textbox):
    def __init__(self, win):
        super().__init__(win)

    def do_command(self, ch):
        if ch in (curses.KEY_ENTER, 10, 13):
            return 0
        elif ch == 7:  # Ctrl-G to zakończenie
            return 0
        elif ch >= 256:
            # Obsługa polskich znaków
            try:
                self.win.addstr(chr(ch))
            except curses.error:
                pass
        else:
            super().do_command(ch)
        return 1


class Input:
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
        self.box = NotMineTextboxWithUtfSupport(self.input)  # Textbox(self.input)

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
