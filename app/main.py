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

    projects = Projects([
        Project(project["name"], [Task(task["name"]) for task in project["tasks"]]) for project in data["projects"]
    ])

    ui_state = UIState.from_dict(data["ui_state"])

    while True:
        curses.curs_set(0)
        main_window.keypad(True)
        curses.noecho()

        main_window.clear()

        current_project: Project = projects.projects[ui_state.project] \
            if len(projects.projects) > 0 else None

        current_project_task: Task = current_project.tasks[ui_state.project_task] \
            if ui_state.view_type == "task" else None

        # Windows
        full_width = curses.COLS
        smaller_window_height = 5

        projects_header = "Projects list"
        tasks_header = f"Project '{projects.projects[ui_state.project].name}' Tasks List"
        menu_header = "What do you want to do?"
        add_project_input_header = "Insert project name"
        add_project_task_input_header = "Insert project task name"
        change_project_name_input_header = "Change project name"
        change_project_task_name_input_header = "Change project task name"

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

        projects_window = Window(main_window, curses.LINES - smaller_window_height, full_width, 0, 0)
        tasks_window = Window(main_window, curses.LINES - smaller_window_height, full_width, 0, 0)
        projects_menu_window = Window(main_window, smaller_window_height, full_width, curses.LINES - smaller_window_height, 0)
        tasks_menu_window = Window(main_window, smaller_window_height, full_width, curses.LINES - smaller_window_height, 0)
        input_window = InputDialog(main_window)
        confirmation_window = ConfirmationDialog(main_window)

        menu = projects_menu_window if ui_state.view_type == "project" else tasks_menu_window


        if ui_state.mode == "editing":
            curses.start_color()
            curses.init_pair(1, 8, curses.COLOR_BLACK)
            menu.sub_window.bkgd(" ", curses.color_pair(1))
            menu.refresh()

        if ui_state.view_type == "project":
            projects_window.display(
                projects_header,
                "column",
                projects.names,
                ui_state.project
            )

            projects_menu_window.display(
                menu_header,
                "row",
                list(project_menu_options.values()),
                ui_state.menu
            )
        elif ui_state.view_type == "task":
            tasks_window.display(
                tasks_header,
                "column",
                current_project.task_names,
                ui_state.project_task
            )

            tasks_menu_window.display(
                menu_header,
                "row",
                list(task_menu_options.values()),
                ui_state.menu
            )

        # HANDLE KEY FUNCTIONS START
        def confirmation(func):
            def wrapper(*args, **kwargs):
                if confirmation_window.display():
                    func(*args, **kwargs)

            return wrapper

        def input(func):
            def wrapper(*args, **kwargs):
                input_window.display(change_project_task_name_input_header)
                value = input_window.get()

                func(value)

            return  wrapper

        #@input
        def add_project():
            input_window.display(add_project_input_header)
            project_name = input_window.get()

            project = Project(project_name)

            projects.add(project)
            ui_state.project = len(projects.projects) - 1

        @confirmation
        def delete_project():
            projects.delete(ui_state.project)

            if ui_state.project != 0:
                ui_state.project -= 1

        def change_project_name():
            input_window.display(change_project_name_input_header)
            new_project_name = input_window.get()

            projects.projects[ui_state.project].name = new_project_name

        def add_project_task():
            input_window.display(add_project_task_input_header)
            project_task_name = input_window.get()

            task = Task(project_task_name)

            current_project.add_task(task)
            ui_state.project_task = len(current_project.task_names) - 1

        @confirmation
        def delete_project_task():
            current_project.delete_task(ui_state.project_task)

            if ui_state.project_task != 0:
                ui_state.project_task -= 1

        def change_project_task_name():
            input_window.display(change_project_task_name_input_header)
            new_project_task_name = input_window.get()

            current_project.tasks[ui_state.project_task].name = new_project_task_name

        @confirmation
        def exit_app():
            quit()
        # HANDLE KEY FUNCTIONS END

        pressed_key = listen_for_key_input(main_window)

        # zamiast ui_state.selected_project_position to np. current_item
        # zamiast current_project.task_names to np. current_item_tasks
        # ITP! ujednolicając przy uruchomieniu while obecny projekt i obecne zadanie
        if ui_state.mode == "editing" and ui_state.view_type == "project" and current_project is not None:
            upper_project = projects.projects[ui_state.project - 1] \
                if ui_state.project > 0 else None

            lower_project = projects.projects[ui_state.project + 1] \
                if ui_state.project < len(projects.names) - 1 else None

            match pressed_key:
                case curses.KEY_UP:
                    if upper_project is not None:
                        projects.projects[ui_state.project] = upper_project
                        projects.projects[ui_state.project - 1] = current_project
                        ui_state.project -= 1
                case curses.KEY_DOWN:
                    if lower_project is not None:
                        projects.projects[ui_state.project] = lower_project
                        projects.projects[ui_state.project + 1] = current_project
                        ui_state.project += 1
                case curses.KEY_ENTER | 10 | 13:
                    ui_state.mode = "normal"
        elif (ui_state.mode == "editing"
                and ui_state.view_type == "task"
                and current_project_task is not None):
            upper_project_task = current_project.tasks[ui_state.project_task - 1] \
                if ui_state.project_task > 0 else None

            lower_project_task = current_project.tasks[ui_state.project_task + 1] \
                if ui_state.project_task < len(current_project.task_names) - 1 else None

            match pressed_key:
                case curses.KEY_UP:
                    if upper_project_task is not None:
                        current_project.tasks[ui_state.project_task] = upper_project_task
                        current_project.tasks[ui_state.project_task - 1] = current_project_task
                        ui_state.project_task -= 1
                case curses.KEY_DOWN:
                    if lower_project_task is not None:
                        current_project.tasks[ui_state.project_task] = lower_project_task
                        current_project.tasks[ui_state.project_task + 1] = current_project_task
                        ui_state.project_task += 1
                case curses.KEY_ENTER | 10 | 13:
                    ui_state.mode = "normal"
        elif ui_state.mode == "normal" and ui_state.view_type == "project":
            match pressed_key:
                case curses.KEY_LEFT if ui_state.menu > 0:
                    ui_state.menu -= 1
                case curses.KEY_RIGHT if ui_state.menu < len(list(project_menu_options.values())) - 1:
                    ui_state.menu += 1
                case curses.KEY_UP if ui_state.project > 0:
                    ui_state.project -= 1
                case curses.KEY_DOWN if ui_state.project < len(projects.names) - 1:
                    ui_state.project += 1
                case curses.KEY_ENTER | 10 | 13:  # enter_key numbers in various systems
                    match ProjectActions(ui_state.menu):
                        case ProjectActions.OPEN:
                            ui_state.view_type = "task"
                        case ProjectActions.ADD:
                            add_project()
                        case ProjectActions.DELETE:
                            delete_project()
                        case ProjectActions.CHANGE_NAME:
                            change_project_name()
                        case ProjectActions.CHANGE_POSITION:
                            ui_state.mode = "editing"
                        case ProjectActions.EXIT:
                            exit_app()
        elif ui_state.mode == "normal" and ui_state.view_type == "task":
            match pressed_key:
                case curses.KEY_LEFT if ui_state.menu > 0:
                    # previous_menu_option
                    ui_state.menu -= 1
                case curses.KEY_RIGHT if ui_state.menu < len(list(task_menu_options.values())) - 1:
                    # next_menu_option
                    ui_state.menu += 1
                case curses.KEY_UP if ui_state.project_task > 0:
                    ui_state.project_task -= 1
                case curses.KEY_DOWN if ui_state.project_task < len(current_project.task_names) - 1:
                    ui_state.project_task += 1
                case curses.KEY_ENTER | 10 | 13:  # enter_key numbers in various systems
                    match ProjectTaskActions(ui_state.menu):
                        case ProjectTaskActions.ADD:
                            add_project_task()
                        case ProjectTaskActions.DELETE:
                            delete_project_task()
                        case ProjectTaskActions.CHANGE_NAME:
                            change_project_task_name()
                        case ProjectTaskActions.CHANGE_POSITION:
                            ui_state.mode = "editing"
                        case ProjectTaskActions.CLOSE:
                            ui_state.view_type = "project"

        new_data = ui_state.serialize() | projects.serialize()
        Data.save(data_path, new_data)


if __name__ == "__main__":
    curses.wrapper(main)
