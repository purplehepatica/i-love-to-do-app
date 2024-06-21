import curses

from helpers.helpers import listen_for_key_input, ProjectActions, ProjectTaskActions, confirmation
from components.confirmation_dialog import ConfirmationDialog
from components.input_dialog import InputDialog
from components.windowx import WindowX
from features.ui_state import UIState
from data.data import Data
from features.task import Task
from features.project import Project
from features.projects import Projects


def main(main_window: "curses.window"):
    COLOR_GREY = 8

    curses.start_color()
    curses.init_pair(1, COLOR_GREY, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    data_path = "data/data.json"
    data = Data.load(data_path)

    ui_state = UIState()

    projects = Projects([
        Project(project["name"], [Task(task["name"]) for task in project["tasks"]]) for project in data["projects"]
    ])

    # CONSTANTS
    project_menu_options = [
        "Open",
        "Add",
        "Delete",
        "Change name",
        "Change position",
        "Exit"
    ]

    task_menu_options = [
        "Add",
        "Delete",
        "Change name",
        "Change position",
        "Go back"
    ]

    # WINDOWS CREATION start
    full_width = curses.COLS
    smaller_window_height = 5

    top_items_window = WindowX(
        main_window,
        curses.LINES - smaller_window_height,
        full_width,
        0,
        0
    )

    bottom_menu_window = WindowX(
        main_window,
        smaller_window_height,
        full_width,
        curses.LINES - smaller_window_height,
        0
    )

    input_window = InputDialog(main_window)
    confirmation_window = ConfirmationDialog(main_window)
    # WINDOWS CREATION end

    while True:
        curses.curs_set(0)
        main_window.keypad(True)
        curses.noecho()
        main_window.clear()

        current_project: Project = projects.get(ui_state.project_position) \
            if len(projects.projects) > 0 \
            else None

        current_project_task: Task = current_project.get_task(ui_state.project_task_position) \
            if ui_state.view_type == "task" and len(current_project.tasks) > 0 \
            else None

        current_item = current_project if ui_state.view_type == "project" else current_project_task
        ui_state.current_item_position = ui_state.project_position if ui_state.view_type == "project" \
            else ui_state.project_task_position

        items = projects.projects if ui_state.view_type == "project" else current_project.tasks
        items_names = projects.names if ui_state.view_type == "project" else current_project.task_names

        upper_item = items[ui_state.current_item_position - 1] if len(items) > 0 \
            else None
        lower_item = items[ui_state.current_item_position + 1] if ui_state.current_item_position < len(items) - 1 \
            else None

        menu_options = project_menu_options \
            if ui_state.view_type == "project" \
            else task_menu_options

        items_header = "Projects list" \
            if ui_state.view_type == "project" \
            else f"Project '{current_project.name}' Tasks List"

        menu_header = "What do you want to do?"

        add_item_header = "Insert project name" if ui_state.view_type == "project" \
            else "Insert project task name"

        change_item_name_header = "Change project name" if ui_state.view_type == "project" \
            else "Change project task name"

        curses_color_pair = 1 if ui_state.mode == "editing" else 2
        bottom_menu_window.sub_window.bkgd(" ", curses.color_pair(curses_color_pair))

        top_items_window.display(
            items_header,
            "column",
            items_names,
            ui_state.current_item_position
        )

        bottom_menu_window.display(
            menu_header,
            "row",
            menu_options,
            ui_state.menu_position
        )

        # HANDLE KEY FUNCTIONS START
        def add_item():
            input_window.display(add_item_header)
            item_name = input_window.get()

            if item_name == "":
                return

            new_item = Project(item_name) if ui_state.view_type == "project" else Task(item_name)
            projects.add(new_item) if ui_state.view_type == "project" else current_project.add_task(new_item)

            ui_state.current_item_position = len(items) - 1

        @confirmation(confirmation_window)
        def delete_item():
            projects.delete(ui_state.project_position) if ui_state.view_type == "project" \
                else current_project.delete_task(ui_state.project_task_position)

            if ui_state.current_item_position > 0:
                ui_state.current_item_position -= 1

        def change_item_name():
            input_window.display(change_item_name_header)
            new_item_name = input_window.get()

            if new_item_name == "":
                return

            current_item.name = new_item_name
        # HANDLE KEY FUNCTIONS END

        # KEYS LOGIC
        pressed_key = listen_for_key_input(main_window)

        # HANDLE APP MODES
        if ui_state.mode == "editing":
            match pressed_key:
                case curses.KEY_UP if upper_item is not None:
                    # move_item_up
                    items[ui_state.current_item_position] = upper_item
                    items[ui_state.current_item_position - 1] = current_item
                    ui_state.current_item_position -= 1
                case curses.KEY_DOWN if lower_item is not None:
                    # move_item_down
                    items[ui_state.current_item_position] = lower_item
                    items[ui_state.current_item_position + 1] = current_item
                    ui_state.current_item_position += 1
                case curses.KEY_ENTER | 10 | 13:
                    # change mode to normal
                    ui_state.mode = "normal"
                    continue
        elif ui_state.mode == "normal":
            match pressed_key:
                case curses.KEY_LEFT if ui_state.menu_position > 0:
                    # previous_menu_option
                    ui_state.menu_position -= 1
                case curses.KEY_RIGHT if ui_state.menu_position < len(menu_options) - 1:
                    # next_menu_option
                    ui_state.menu_position += 1
                case curses.KEY_UP if ui_state.current_item_position > 0:
                    # select_upper_item
                    ui_state.current_item_position -= 1
                case curses.KEY_DOWN if ui_state.current_item_position < len(items) - 1:
                    # select_bottom item
                    ui_state.current_item_position += 1
                case curses.KEY_ENTER | 10 | 13:  # enter key numbers in various systems
                    # HANDLE ENTER PRESS BASED ON VIEW_TYPE
                    if ui_state.view_type == "project":
                        match ProjectActions(ui_state.menu_position):
                            case ProjectActions.OPEN if current_project is not None:
                                ui_state.view_type = "task"
                            case ProjectActions.ADD:
                                add_item()
                            case ProjectActions.DELETE if current_project is not None:
                                delete_item()
                            case ProjectActions.CHANGE_NAME if current_project is not None:
                                change_item_name()
                            case ProjectActions.CHANGE_POSITION if current_project is not None:
                                ui_state.mode = "editing"
                            case ProjectActions.EXIT if confirmation_window.display():
                                quit()
                    elif ui_state.view_type == "task":
                        match ProjectTaskActions(ui_state.menu_position):
                            case ProjectTaskActions.ADD:
                                add_item()
                            case ProjectTaskActions.DELETE if current_project_task is not None:
                                delete_item()
                            case ProjectTaskActions.CHANGE_NAME if current_project_task is not None:
                                change_item_name()
                            case ProjectTaskActions.CHANGE_POSITION if current_project_task is not None:
                                ui_state.mode = "editing"
                            case ProjectTaskActions.CLOSE:
                                ui_state.view_type = "project"
                                ui_state.menu_position = 0
                                ui_state.current_item_position = ui_state.project_position
                                continue

        if ui_state.view_type == "project":
            ui_state.project_position = ui_state.current_item_position
        elif ui_state.view_type == "task":
            ui_state.project_task_position = ui_state.current_item_position

        new_data = projects.serialize()
        Data.save(data_path, new_data)


if __name__ == "__main__":
    curses.wrapper(main)
