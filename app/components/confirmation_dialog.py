import curses


class ConfirmationDialog:
    def __init__(self, main_window: "curses.window"):
        self.window = main_window

    def display(self):
        self.window.clear()

        self.window.border()

        self.window.addstr((curses.LINES // 2) - 3, 1, "--- Czy jesteś pewien? ---".center(curses.COLS - 2).upper())

        selected_modal_option = 0

        options = ["TAK", "NIE"]

        while True:
            self.window.addstr((curses.LINES // 2) - 1, 1, "")
            # Centrowanie menu: do poprawy
            options_length = 0

            for option in options:
                options_length += len(option) + 2

            self.window.addstr(" " * ((curses.COLS - options_length) // 2))
            # Koniec centrowania menu

            for i, item in enumerate(options):
                attribute = curses.A_REVERSE if i == selected_modal_option else curses.A_NORMAL

                self.window.addstr(f" {item} ", attribute)

            pressed_key = self.window.getch()

            match pressed_key:
                case curses.KEY_LEFT if selected_modal_option == 1:
                    selected_modal_option -= 1
                case curses.KEY_RIGHT if selected_modal_option == 0:
                    selected_modal_option += 1
                case curses.KEY_ENTER | 10 | 13:
                    self.window.clear()
                    return True if selected_modal_option == 0 else False
