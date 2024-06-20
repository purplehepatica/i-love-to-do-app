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

    # WINDOWS CREATION
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

        menu_options = list(project_menu_options.values()) \
            if ui_state.view_type == "project" \
            else list(task_menu_options.values())

        items_header = "Projects list" \
            if ui_state.view_type == "project" \
            else f"Project '{current_project.name}' Tasks List"

        menu_header = "What do you want to do?"

        add_item_header = "Insert project name" if ui_state.view_type == "project" \
            else "Insert project task name"

        change_item_name_header = "Change project name" if ui_state.view_type == "project" \
            else "Change project task name"

        items = projects.projects if ui_state.view_type == "project" else current_project.tasks
        items_names = projects.names if ui_state.view_type == "project" else current_project.task_names

        current_item = current_project if ui_state.view_type == "project" else current_project_task

        current_item_position = ui_state.project_position if ui_state.view_type == "project" \
            else ui_state.project_task_position

        if ui_state.mode == "editing":
            curses.start_color()
            curses.init_pair(1, 8, curses.COLOR_BLACK)
            bottom_menu_window.sub_window.bkgd(" ", curses.color_pair(1))
        elif ui_state.mode == "normal":
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            bottom_menu_window.sub_window.bkgd(" ", curses.color_pair(1))

        top_items_window.display(
            items_header,
            "column",
            items_names,
            current_item_position
        )

        bottom_menu_window.display(
            menu_header,
            "row",
            menu_options,
            ui_state.menu_position
        )

        # HANDLE KEY FUNCTIONS START
        def change_item_name():
            input_window.display(change_item_name_header)
            new_item_name = input_window.get()

            if new_item_name == "":
                return

            current_item.name = new_item_name
        # HANDLE KEY FUNCTIONS END

        # KEYS LOGIC
        upper_item = items[current_item_position - 1] if current_item_position > 0 else None
        lower_item = items[current_item_position + 1] if current_item_position < len(items) - 1 else None

        pressed_key = listen_for_key_input(main_window)

        # HANDLE APP MODES
        if ui_state.mode == "editing":
            match pressed_key:
                case curses.KEY_UP if upper_item is not None:
                    # move_item_up
                    items[current_item_position] = upper_item
                    items[current_item_position - 1] = current_item
                    current_item_position -= 1
                case curses.KEY_DOWN if lower_item is not None:
                    # move_item_down
                    items[current_item_position] = lower_item
                    items[current_item_position + 1] = current_item
                    current_item_position += 1
                case curses.KEY_ENTER | 10 | 13:
                    # change mode to normal
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
                    # select_upper_item
                    current_item_position -= 1
                case curses.KEY_DOWN if current_item_position < len(items) - 1:
                    # select_bottom item
                    current_item_position += 1
                case curses.KEY_ENTER | 10 | 13:  # enter key numbers in various systems
                    # HANDLE ENTER PRESS BASED ON VIEW_TYPE
                    if ui_state.view_type == "project":
                        match ProjectActions(ui_state.menu_position):
                            case ProjectActions.OPEN if current_project is not None:
                                ui_state.view_type = "task"
                            case ProjectActions.ADD:
                                input_window.display(add_item_header)
                                project_name = input_window.get()

                                if project_name == "":
                                    return

                                project = Project(project_name)

                                projects.add(project)
                                current_item_position = len(projects.projects) - 1
                            case ProjectActions.DELETE if current_project is not None and confirmation_window.display():
                                projects.delete(ui_state.project_position)

                                if current_item_position > 0:
                                    current_item_position -= 1
                            case ProjectActions.CHANGE_NAME if current_project is not None:
                                change_item_name()
                            case ProjectActions.CHANGE_POSITION if current_project is not None:
                                ui_state.mode = "editing"
                            case ProjectActions.EXIT if confirmation_window.display():
                                quit()
                    elif ui_state.view_type == "task":
                        match ProjectTaskActions(ui_state.menu_position):
                            case ProjectTaskActions.ADD:
                                input_window.display(add_item_header)
                                project_task_name = input_window.get()

                                if project_task_name == "":
                                    return

                                task = Task(project_task_name)

                                current_project.add_task(task)
                                ui_state.project_task_position = len(current_project.task_names) - 1
                            case ProjectTaskActions.DELETE if current_project_task is not None and confirmation_window.display():
                                current_project.delete_task(ui_state.project_task_position)

                                if upper_item is not None:
                                    current_item_position -= 1
                            case ProjectTaskActions.CHANGE_NAME if current_project_task is not None:
                                change_item_name()
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
