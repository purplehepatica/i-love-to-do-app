import curses

from helpers.helpers import listen_for_key_input, ProjectActions, ProjectTaskActions
from components.confirmation_dialog import ConfirmationDialog
from components.input_dialog import InputDialog
from components.window import Window
from features.ui_state import UIState
from data.data import Data
from features.task import Task
from features.project import Project
from features.projects import Projects


def main(main_window: "curses.window"):
    data_path = "data/data.json"
    data = Data.load(data_path)

    ui_state = UIState.from_dict(data["ui_state"])
    projects = Projects([
        Project(project["name"], [Task(task["name"]) for task in project["tasks"]]) for project in data["projects"]
    ])

    # CONSTANTS
    project_menu_options = {
        0: "Open",
        1: "Add",
        2: "Delete",
        3: "Change name",
        4: "Change position",
        5: "Exit"
    }

    task_menu_options = {
        0: "Add",
        1: "Delete",
        2: "Change name",
        3: "Change position",
        4: "Back"
    }

    # HANDLE KEY FUNCTIONS START
    def confirmation(func):
        def wrapper(*args, **kwargs):
            if confirmation_window.display():
                func(*args, **kwargs)

        return wrapper

    def input(func):
        def wrapper(*args, **kwargs):
            input_window.display(change_item_name_header)
            value = input_window.get()

            func(value)

        return wrapper

    # @input
    def add_project():
        input_window.display(add_item_header)
        project_name = input_window.get()

        project = Project(project_name)

        projects.add(project)
        ui_state.project_position -= len(projects.projects) - 1

    @confirmation
    def delete_project():
        projects.delete(ui_state.project_position)

        if ui_state.project_position != 0:
            ui_state.project_position -= 1

    def change_project_name():
        input_window.display(change_item_name_header)
        new_project_name = input_window.get()

        current_project.name = new_project_name

    def add_project_task():
        input_window.display(add_item_header)
        project_task_name = input_window.get()

        task = Task(project_task_name)

        current_project.add_task(task)
        ui_state.project_task_position = len(current_project.task_names) - 1

    @confirmation
    def delete_project_task():
        current_project.delete_task(ui_state.project_task_position)

        if ui_state.project_task_position > 0:
            ui_state.project_task_position -= 1

    def change_project_task_name():
        input_window.display(change_item_name_header)
        new_project_task_name = input_window.get()

        current_project_task.name = new_project_task_name

    @confirmation
    def exit_app():
        quit()
    # HANDLE KEY FUNCTIONS END

    while True:
        curses.curs_set(0)
        main_window.keypad(True)
        curses.noecho()

        current_project: Project = projects.projects[ui_state.project_position] \
            if len(projects.projects) > 0 \
            else None

        current_project_task: Task = current_project.tasks[ui_state.project_task_position] \
            if ui_state.view_type == "task" and len(current_project.tasks) > 0 \
            else None

        # Windows
        full_width = curses.COLS
        smaller_window_height = 5

        projects_window = Window(main_window, curses.LINES - smaller_window_height, full_width, 0, 0)
        tasks_window = Window(main_window, curses.LINES - smaller_window_height, full_width, 0, 0)
        projects_menu_window = Window(main_window, smaller_window_height, full_width, curses.LINES - smaller_window_height, 0)
        tasks_menu_window = Window(main_window, smaller_window_height, full_width, curses.LINES - smaller_window_height, 0)
        input_window = InputDialog(main_window)
        confirmation_window = ConfirmationDialog(main_window)

        menu = projects_menu_window if ui_state.view_type == "project" else tasks_menu_window
        menu_options = list(project_menu_options.values()) if ui_state.view_type == "project" else list(task_menu_options.values())

        items_header = "Projects list" \
            if ui_state.view_type == "project" \
            else f"Project '{current_project.name}' Tasks List"

        menu_header = "What do you want to do?"

        add_item_header = "Insert project name" if ui_state.view_type == "project" \
            else "Insert project task name"

        change_item_name_header = "Change project name" if ui_state.view_type == "project" \
            else "Change project task name"

        items_window = projects_window if ui_state.view_type == "project" else tasks_window
        items = projects.projects if ui_state.view_type == "project" else current_project.tasks
        items_names = projects.names if ui_state.view_type == "project" else current_project.task_names

        current_item = current_project if ui_state.view_type == "project" else current_project_task

        current_item_position = ui_state.project_position if ui_state.view_type == "project" \
            else ui_state.project_task_position

        if ui_state.mode == "editing":
            curses.start_color()
            curses.init_pair(1, 8, curses.COLOR_BLACK)
            menu.sub_window.bkgd(" ", curses.color_pair(1))
            menu.refresh()

        items_window.display(
            items_header,
            "column",
            items_names,
            current_item_position
        )

        menu.display(
            menu_header,
            "row",
            menu_options,
            ui_state.menu_position
        )

        # KEYS LOGIC
        upper_item = items[current_item_position - 1] if current_item_position > 0 else None
        lower_item = items[current_item_position + 1] if current_item_position < len(items) - 1 else None

        pressed_key = listen_for_key_input(main_window)

        if ui_state.mode == "editing":

            match pressed_key:
                case curses.KEY_UP if upper_item is not None:
                    items[current_item_position] = upper_item
                    items[current_item_position - 1] = current_item
                    current_item_position -= 1
                case curses.KEY_DOWN if lower_item is not None:
                    items[current_item_position] = lower_item
                    items[current_item_position + 1] = current_item
                    current_item_position += 1
                case curses.KEY_ENTER | 10 | 13:
                    ui_state.mode = "normal"

        elif ui_state.mode == "normal":

            match pressed_key:
                case curses.KEY_LEFT if ui_state.menu_position > 0:
                    # previous_menu_option
                    ui_state.menu_position -= 1
                case curses.KEY_RIGHT if ui_state.menu_position < len(menu_options) - 1:
                    # next_menu_option
                    ui_state.menu_position += 1
                case curses.KEY_UP if current_item_position > 0:
                    current_item_position -= 1
                case curses.KEY_DOWN if current_item_position < len(items) - 1:
                    current_item_position += 1
                case curses.KEY_ENTER | 10 | 13:  # enter_key numbers in various systems
                    if ui_state.view_type == "project":
                        match ProjectActions(ui_state.menu_position):
                            case ProjectActions.OPEN if current_project is not None:
                                ui_state.view_type = "task"
                            case ProjectActions.ADD:
                                add_project()
                            case ProjectActions.DELETE if current_project is not None:
                                delete_project()
                            case ProjectActions.CHANGE_NAME if current_project is not None:
                                change_project_name()
                            case ProjectActions.CHANGE_POSITION if current_project is not None:
                                ui_state.mode = "editing"
                            case ProjectActions.EXIT:
                                exit_app()
                    elif ui_state.view_type == "task":
                        match ProjectTaskActions(ui_state.menu_position):
                            case ProjectTaskActions.ADD:
                                add_project_task()
                            case ProjectTaskActions.DELETE if current_project_task is not None:
                                delete_project_task()
                            case ProjectTaskActions.CHANGE_NAME if current_project_task is not None:
                                change_project_task_name()
                            case ProjectTaskActions.CHANGE_POSITION if current_project_task is not None:
                                ui_state.mode = "editing"
                            case ProjectTaskActions.CLOSE:
                                ui_state.view_type = "project"
                                ui_state.project_task_position = None

        if ui_state.view_type == "project":
            ui_state.project_position = current_item_position
        elif ui_state.view_type == "task":
            ui_state.project_task_position = current_item_position

        new_data = ui_state.serialize() | projects.serialize()
        Data.save(data_path, new_data)

        main_window.clear()


if __name__ == "__main__":
    curses.wrapper(main)
