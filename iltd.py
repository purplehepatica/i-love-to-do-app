import os

columns, lines = os.get_terminal_size()
seen_lines = lines - 3

def start_full_screen_print():

    print(columns * '=')

    for line in range(seen_lines):
    
        if line == 0 or line == seen_lines - 1:
            print(f"= {(columns - 4) * ' '} =")
        else:
            print(f"=   {(columns - 8) * ' '}   =")

    print(columns * '=')


def initApp():
    start_full_screen_print()

initApp()


projects = {}


max_project_id = 0

def get_max_project_id():
    global  max_project_id
    return max_project_id

def increase_max_project_id():
    global max_project_id
    max_project_id += 1



def init_project_creation():
    project_name = get_project_name()
    project_entry = create_project_entry(project_name)
    project_id = get_max_project_id()
    
    create_project(project_id, project_entry)
    
    increase_max_project_id()

    print(projects)
    return True


def get_project_name():
    return input("Jak nazwiesz swój nowy projekt?: ")

def create_project_entry(project_name):
    return {
        'name': project_name
    }

def create_project(project_id, project_entry):
    projects[project_id] = project_entry



def user_choice():
    choice = ""

    while choice != "p" and choice != "w":
        choice = input("Co chcesz wykonać (p - nowy projekt, w - wyjście)?: ")

    if choice == "p":
        init_project_creation()
        user_choice()
    elif choice == "w":
        quit()

user_choice()
