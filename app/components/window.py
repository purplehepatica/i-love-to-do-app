import curses


class Window:
    def __init__(self, main_window, height, width, begin_y, begin_x):
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x

        self.window = main_window
        self.sub_window = main_window.subwin(self.height, self.width, self.begin_y, self.begin_x)

    def clear(self):
        self.sub_window.clear()
        self.sub_window.refresh()

    def refresh(self):
        self.sub_window.refresh()

    def display(self, header, direction, items, current_item):
        self.sub_window.border()

        self.sub_window.addstr(1, 1, f"--- {header} ---".center(self.width - 2).upper(), curses.A_BOLD)
        self.sub_window.addstr(2, 1, "-" * (self.width - 2))
        self.sub_window.addstr(3, 1, "")

        # Centrowanie menu: do poprawy
        if direction == "row":
            items_length = 0

            for item in items:
                items_length += len(item) + 2 + 4

            self.sub_window.addstr(" " * ((curses.COLS - items_length) // 2))
        # Koniec centrowania menu

        for i, item in enumerate(items):
            attribute = curses.A_REVERSE | curses.A_BOLD if i == current_item else curses.A_DIM

            if direction == "column":
                self.sub_window.addstr(3 + i, 1, f"{i + 1}. {item}".center(self.width - 2).upper(), attribute)
            elif direction == "row":
                self.sub_window.addstr(f" {i + 1}. {item} ".upper(), attribute)

        self.sub_window.refresh()
        self.window.refresh()
