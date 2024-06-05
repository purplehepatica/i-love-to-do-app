import os


class ScreenBuffer:
    @property
    def columns(self) -> int:
        return os.get_terminal_size().columns

    @property
    def lines(self) -> int:
        return os.get_terminal_size().lines - 1

    def display(self, content: list[str]) -> None:
        os.system('clear')

        content_length = len(content)

        first_line = 0
        last_line = self.lines - 1

        for line in range(self.lines):
            if line == first_line or line == last_line:
                print(self.columns * '=')
            elif line == 3:
                print("=", "--- LISTA PROJEKTÓW ---".center(self.columns - 4), "=")
            elif 5 <= line <= 5 + content_length and content_length > 0 and line - 5 < content_length:
                print("=", f"{line - 5}. {content[line - 5]}".center(self.columns - 4), "=")
            else:
                print("=", (self.columns - 4) * ' ', "=")
