import curses

from components.modal import Modal
from components.input import Input
from components.window import Window
from features.selections_state import SelectionsState
from data.data import Data
from features.task import Task
from features.project import Project
from features.projects import Projects


def listen_for_key_input(main_window: "curses.window"):
    return main_window.getch()


def main(main_window: "curses.window"):
    data_path = "data/data.json"
    data = Data.load(data_path)

    projects = Projects([
        Project(project["name"], [Task(task["name"]) for task in project["tasks"]]) for project in data["projects"]
    ])

    selected_positions = SelectionsState()
    selected_positions.selected_project_position = data["selected_positions"]["selected_project_position"]
    selected_positions.selected_menu_option = data["selected_positions"]["selected_menu_option"]

    while True:
        curses.curs_set(0)
        main_window.keypad(True)
        curses.noecho()

        current_project = projects.projects[selected_positions.selected_project_position] if len(projects.projects) > 0 else None

        # Windows
        full_width = curses.COLS
        smaller_window_height = 5

        projects_header = "Projects list"
        tasks_header = f"Project '{projects.projects[selected_positions.selected_project_position].name}' Tasks List"
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

        project_task_menu_options = {
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
        input_window = Input(main_window)
        confirmation_window = Modal(main_window)

        if selected_positions.view_type == "project":
            projects_window.display(
                projects_header,
                "column",
                projects.names,
                selected_positions.selected_project_position
            )

            projects_menu_window.display(
                menu_header,
                "row",
                list(project_menu_options.values()),
                selected_positions.selected_menu_option
            )
        elif selected_positions.view_type == "task":
            tasks_window.display(
                tasks_header,
                "column",
                current_project.task_names,
                selected_positions.selected_project_task_position
            )

            tasks_menu_window.display(
                menu_header,
                "row",
                list(project_task_menu_options.values()),
                selected_positions.selected_menu_option
            )

        # Pressed Keys Management
        def confirmation(func):
            def wrapper(*args, **kwargs):
                if confirmation_window.display():
                    func(*args, **kwargs)

            return wrapper

        def open_project():
            main_window.clear()
            selected_positions.view_type = "task"

        def close_project():
            main_window.clear()
            selected_positions.view_type = "project"

        def add_project():
            input_window.display(add_project_input_header)
            project_name = input_window.get()

            project = Project(project_name)

            projects.add(project)
            selected_positions.selected_project_position = len(projects.projects) - 1

        @confirmation
        def delete_project():
            projects.delete(selected_positions.selected_project_position)
            main_window.clear()

            if selected_positions.selected_project_position != 0:
                selected_positions.selected_project_position -= 1

        def change_project_name():
            input_window.display(change_project_name_input_header)
            new_project_name = input_window.get()

            projects.projects[selected_positions.selected_project_position].name = new_project_name

        def change_project_position():
            # np. if view_type == "project_position_change"
            curses.start_color()
            curses.init_pair(1, 8, curses.COLOR_BLACK)
            projects_menu_window.sub_window.bkgd(" ", curses.color_pair(1))
            projects_menu_window.refresh()

            while True:
                current_project = projects.projects[selected_positions.selected_project_position]

                upper_project = projects.projects[selected_positions.selected_project_position - 1] \
                    if selected_positions.selected_project_position > 0 else None

                lower_project = projects.projects[selected_positions.selected_project_position + 1] \
                    if selected_positions.selected_project_position < len(projects.names) - 1 else None

                key = main_window.getch()

                match key:
                    case curses.KEY_UP:
                        if upper_project is not None:
                            projects.projects[selected_positions.selected_project_position] = upper_project
                            projects.projects[selected_positions.selected_project_position - 1] = current_project
                            selected_positions.selected_project_position -= 1
                    case curses.KEY_DOWN:
                        if lower_project is not None:
                            projects.projects[selected_positions.selected_project_position] = lower_project
                            projects.projects[selected_positions.selected_project_position + 1] = current_project
                            selected_positions.selected_project_position += 1
                    case curses.KEY_ENTER | 10 | 13:
                        break

                projects_window.display(
                    projects_header,
                    "column",
                    projects.names,
                    selected_positions.selected_project_position
                )

        def add_project_task():
            input_window.display(add_project_task_input_header)
            project_task_name = input_window.get()

            task = Task(project_task_name)

            current_project.add_task(task)
            selected_positions.selected_project_task_position = len(current_project.task_names) - 1

        @confirmation
        def delete_project_task():
            current_project.delete_task(selected_positions.selected_project_task_position)
            main_window.clear()

            if selected_positions.selected_project_task_position != 0:
                selected_positions.selected_project_task_position -= 1

        def change_project_task_name():
            input_window.display(change_project_task_name_input_header)
            new_project_task_name = input_window.get()

            current_project.tasks[selected_positions.selected_project_task_position].name = new_project_task_name

        def change_project_task_position():
            # np. if view_type == "project_task_position_change" -> lub całkowicie ujednolicić
            curses.start_color()
            curses.init_pair(1, 8, curses.COLOR_BLACK)
            tasks_menu_window.sub_window.bkgd(" ", curses.color_pair(1))
            tasks_menu_window.refresh()

            while True:
                current_project_task = current_project.tasks[selected_positions.selected_project_task_position]

                upper_project_task = current_project.tasks[selected_positions.selected_project_task_position - 1] \
                    if selected_positions.selected_project_task_position > 0 else None

                lower_project_task = current_project.tasks[selected_positions.selected_project_task_position + 1] \
                    if selected_positions.selected_project_task_position < len(current_project.task_names) - 1 else None

                key = main_window.getch()

                match key:
                    case curses.KEY_UP:
                        if upper_project_task is not None:
                            current_project.tasks[selected_positions.selected_project_task_position] = upper_project_task
                            current_project.tasks[selected_positions.selected_project_task_position - 1] = current_project_task
                            selected_positions.selected_project_task_position -= 1
                    case curses.KEY_DOWN:
                        if lower_project_task is not None:
                            current_project.tasks[selected_positions.selected_project_task_position] = lower_project_task
                            current_project.tasks[selected_positions.selected_project_task_position + 1] = current_project_task
                            selected_positions.selected_project_task_position += 1
                    case curses.KEY_ENTER | 10 | 13:
                        break

                tasks_window.display(
                    tasks_header,
                    "column",
                    current_project.task_names,
                    selected_positions.selected_project_task_position
                )

        @confirmation
        def exit_app():
            quit()

        project_actions = {
            0: open_project,
            1: add_project,
            2: delete_project,
            3: change_project_name,
            4: change_project_position,
            5: exit_app
        }

        project_task_actions = {
            0: add_project_task,
            1: delete_project_task,
            2: change_project_task_name,
            3: change_project_task_position,
            4: close_project,
        }

        pressed_key = listen_for_key_input(main_window)

        # zamiast selected_positions.selected_project_position to np. current_item
        # zamiast current_project.task_names to np. current_item_tasks
        # ITP! ujednolicając przy uruchomieniu while obecny projekt i obecne zadanie
        if selected_positions.view_type == "project":
            match pressed_key:
                case curses.KEY_LEFT if selected_positions.selected_menu_option > 0:
                    selected_positions.selected_menu_option -= 1
                case curses.KEY_RIGHT if selected_positions.selected_menu_option < len(list(project_menu_options.values())) - 1:
                    selected_positions.selected_menu_option += 1
                case curses.KEY_UP if selected_positions.selected_project_position > 0:
                    selected_positions.selected_project_position -= 1
                case curses.KEY_DOWN if selected_positions.selected_project_position < len(projects.names) - 1:
                    selected_positions.selected_project_position += 1
                case curses.KEY_ENTER | 10 | 13:  # enter_key numbers in various systems
                    action = project_actions[selected_positions.selected_menu_option]
                    action()
        elif selected_positions.view_type == "task":
            match pressed_key:
                case curses.KEY_LEFT if selected_positions.selected_menu_option > 0:
                    selected_positions.selected_menu_option -= 1
                case curses.KEY_RIGHT if selected_positions.selected_menu_option < len(list(project_task_menu_options.values())) - 1:
                    selected_positions.selected_menu_option += 1
                case curses.KEY_UP if selected_positions.selected_project_task_position > 0:
                    selected_positions.selected_project_task_position -= 1
                case curses.KEY_DOWN if selected_positions.selected_project_task_position < len(current_project.task_names) - 1:
                    selected_positions.selected_project_task_position += 1
                case curses.KEY_ENTER | 10 | 13:  # enter_key numbers in various systems
                    action = project_task_actions[selected_positions.selected_menu_option]
                    action()

        new_data = selected_positions.serialize() | projects.serialize()
        Data.save(data_path, new_data)


if __name__ == "__main__":
    curses.wrapper(main)
