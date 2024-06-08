import curses

from components.get_input_modal import get_input_modal
from components.display_menu import display_menu
from components.display_projects import display_projects
from components.listen_for_key_input import listen_for_key_input
from data.data import Data
from features.projects import Projects


def main(main_window: "curses.window") -> None:
    data_path = "data/data.json"
    data = Data(data_path)
    data.load()

    while True:
        # curses.start_color()
        # COLOR_SLATE_BLUE_3 = 61
        # curses.init_pair(1, curses.COLOR_WHITE, COLOR_SLATE_BLUE_3)
        # stdscr.bkgd(" ", curses.color_pair(1))

        projects = Projects(data.projects)

        # -> state = State(data.state)

        # zapobiec sytuacji, gdy pliku nie ma lub jest wypełniony innymi danymi
        # !!!
        # operacje na state, np.
        # increase_menu_choice_position()
        # decrease_menu_choice_position()
        # increase_current_project_position()
        # decrease_current_project_position()
        current_project = data.state["current_project"]
        current_choice = data.state["current_choice"]

        projects_names = projects.names

        display_projects(main_window, projects_names, current_project)

        display_menu(main_window, current_choice)

        key = listen_for_key_input(main_window)

        if key == curses.KEY_LEFT and current_choice > 0:
            data.state["current_choice"] -= 1
            main_window.refresh()
        elif key == curses.KEY_RIGHT and current_choice < 3:
            data.state["current_choice"] += 1
            main_window.refresh()

        if key == curses.KEY_UP and current_project > 0:
            data.state["current_project"] -= 1
            main_window.refresh()
        elif key == curses.KEY_DOWN and current_project < len(projects_names) - 1:
            data.state["current_project"] += 1
            main_window.refresh()

        if key in [curses.KEY_ENTER, 10, 13]:

            match current_choice:
                case 0:
                    main_window.clear()
                    project_name = get_input_modal(main_window)

                    # by po dodaniu projektu focus kierował się właśnie na niego
                    projects.add(project_name)
                case 1:
                    # by po usunięciu projektu focus nie był ustawiony na usuniętym projekcie
                    projects.delete(current_project)
                case 2:
                    data.save()
                case 3:
                    quit()


if __name__ == "__main__":
    curses.wrapper(main)
