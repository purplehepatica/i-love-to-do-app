import curses

from features.selections_state import SelectionsState
from components.get_input_modal import get_input_modal
from components.display_menu import display_menu_window
from components.display_projects import display_projects_window
from components.listen_for_key_input import listen_for_key_input
from data.data import Data
from features.project import Project
from features.projects import Projects


def save_data(data_path, selected_positions, projects):
    selections_state_dict = {
        "selected_positions": selected_positions.__dict__
    }

    projects_dict = {
        "projects": [project.__dict__ for project in projects.projects]
    }

    new_data = selections_state_dict | projects_dict
    Data.save(data_path, new_data)


def main(main_window: "curses.window") -> None:
    data_path = "data/data.json"
    data = Data.load(data_path)

    projects = Projects([
        Project(project["name"]) for project in data["projects"]
    ])

    selected_positions = SelectionsState()
    selected_positions.selected_project_position = data["selected_positions"]["selected_project_position"]
    selected_positions.selected_menu_option = data["selected_positions"]["selected_menu_option"]

    while True:
        main_window.refresh()

        main_window.border()
        curses.curs_set(0)
        main_window.keypad(True)
        curses.noecho()

        display_projects_window(main_window, projects.names, selected_positions.selected_project_position)
        display_menu_window(main_window, selected_positions.selected_menu_option)

        key = listen_for_key_input(main_window)

        if key == curses.KEY_LEFT and selected_positions.selected_menu_option > 0:
            # handle_key_left_press
            selected_positions.selected_menu_option -= 1
        elif key == curses.KEY_RIGHT and selected_positions.selected_menu_option < 3:
            # handle_key_right_press
            selected_positions.selected_menu_option += 1

        if key == curses.KEY_UP and selected_positions.selected_project_position > 0:
            # handle_key_up_press
            selected_positions.selected_project_position -= 1
        elif key == curses.KEY_DOWN and selected_positions.selected_project_position < len(projects.names) - 1:
            # handle_key_down_press
            selected_positions.selected_project_position += 1

        if key in [curses.KEY_ENTER, 10, 13]:
            # handle_enter_key_press

            match selected_positions.selected_menu_option:
                case 0:
                    main_window.clear()
                    project_name = get_input_modal(main_window)
                    project = Project(project_name)

                    projects.add(project)
                    selected_positions.selected_project_position = len(projects.projects) - 1

                    save_data(data_path, selected_positions, projects)
                case 1:
                    projects.delete(selected_positions.selected_project_position)

                    if selected_positions.selected_project_position != 0:
                        selected_positions.selected_project_position -= 1

                    save_data(data_path, selected_positions, projects)
                case 2:
                    quit()


if __name__ == "__main__":
    curses.wrapper(main)
