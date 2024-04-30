import os

# data.py (?)
input_choices = []  # POPRAWIĆ
projects = {}

max_project_id = 0


def get_max_project_id():
    global max_project_id
    return max_project_id


def increase_max_project_id():
    global max_project_id
    max_project_id += 1


# screens.py (?)

columns, lines = os.get_terminal_size()
visible_lines = lines - 3


def display_screen():
    print(columns * '=')

    for line in range(visible_lines):

        if line == 0 or line == visible_lines - 1:
            print(f"= {(columns - 4) * ' '} =")
        elif line == 3:
            print(f"=", "--- LISTA PROJEKTÓW ---".center(columns - 4), "=")
        elif line >= 5 and line <= 5 + max_project_id and max_project_id > 0 and line - 5 in projects:
            print(f"=", f"{line - 5}. {projects[line - 5]["name"]}".center(columns - 4), "=")
        else:
            print(f"=   {(columns - 8) * ' '}   =")

    print(columns * '=')


def refresh_screen():
    display_screen()


# projects.py
def init_project_creation():
    project_name = get_project_name()
    project_entry = create_project_entry(project_name)
    project_id = get_max_project_id()

    create_project(project_id, project_entry)

    increase_max_project_id()


def get_project_name():
    return input("Jak nazwiesz swój nowy projekt?: ")


def get_project_data():
    pass


def create_project_entry(project_name):
    return {
        'name': project_name
    }


def create_project(project_id, project_entry):
    projects[project_id] = project_entry


# inputs.py / user_choice.py (?)

def user_choice():
    choice = ""

    while True:
        while choice != "p" and choice != "w":
            choice = input("Co chcesz wykonać (p - nowy projekt, w - wyjście)?: ")
            refresh_screen()

        if choice == "p":
            init_project_creation()
            refresh_screen()
            choice = ""
        elif choice == "w":
            quit()


def main():
    display_screen()
    user_choice()


if __name__ == "__main__":
    main()
