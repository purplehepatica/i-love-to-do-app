import os
from pynput import keyboard


def clear_screen():
    os.system("clear")


def get_input_modal():
    columns, lines = os.get_terminal_size()

    mid_col = round(columns / 2)
    mid_line = round(lines / 2)

    for line in range(lines):
        if line == mid_line - 3:
            print("\033[4mhello\033[0m")
        if line == mid_line - 2:
            print("Wpisz nazwę projektu:".center(columns))
        elif line == mid_line:
            message = input("> ")
        else:
            print("")


def main():
    while True:
        clear_screen()

        choice = None
        choices = ["1. Hello", "2. World", "3. Wyjdź"]
        #print(" ".join(choices))
        print(keyboard.read_key())


if __name__ == "__main__":
    main()
