import curses
from components.get_input_modal import get_input_modal
from components.display_menu import display_menu
from components.display_projects import display_projects
from components.listen_for_key_input import listen_for_key_input
from data.data import get_data, save_data
from features.project import get_project_names, create_project_entry, add_project, delete_project


def main(main_window: "curses.window") -> None:
    data_path = "data/data.json"
    data = get_data(data_path)

    choice = 0
    current_project = 0

    while True:
        # curses.start_color()
        # COLOR_SLATE_BLUE_3 = 61
        # curses.init_pair(1, curses.COLOR_WHITE, COLOR_SLATE_BLUE_3)
        # stdscr.bkgd(" ", curses.color_pair(1))

        projects_names = get_project_names(data)

        display_projects(main_window, projects_names, current_project)

        display_menu(main_window, choice)

        key = listen_for_key_input(main_window)

        if key == curses.KEY_LEFT and choice > 0:
            choice -= 1
            main_window.refresh()
        elif key == curses.KEY_RIGHT and choice < 3:
            choice += 1
            main_window.refresh()

        if key == curses.KEY_UP and current_project > 0:
            current_project -= 1
            main_window.refresh()
        elif key == curses.KEY_DOWN and current_project < len(projects_names) - 1:
            current_project += 1
            main_window.refresh()

        if key in [curses.KEY_ENTER, 10, 13]:

            match choice:
                case 0:
                    main_window.clear()
                    project_name = get_input_modal(main_window)

                    project_entry = create_project_entry(project_name)

                    add_project(data, project_entry)
                case 1:
                    delete_project(data, current_project)
                case 2:
                    save_data(data_path, data)
                case 3:
                    quit()


if __name__ == "__main__":
    curses.wrapper(main)
