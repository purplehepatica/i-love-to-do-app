import curses


class ProjectsWindow:
    def __init__(self, main_window: "curses.window"):
        self.main_window = main_window

    def create(self):
        pass

    def display(self):
        pass

    def get(self, box):
        pass


def display_projects_window(main_window: "curses.window", projects, current_project):

    main_window.refresh()

    projects_lines = curses.LINES - 5
    projects_columns = curses.COLS

    projects_start_y = 0
    projects_start_x = 0

    projects_window = curses.newwin(
        projects_lines, projects_columns, projects_start_y, projects_start_x
    )

    projects_window.border()

    projects_window.addstr(2, 1, "--- LISTA PROJEKTÓW ---".center(projects_columns - 2))

    for i, project_name in enumerate(projects):
        attribute = curses.A_REVERSE if i == current_project else curses.A_NORMAL

        projects_window.addstr(4 + i, 1, f"{i + 1}. {project_name}".center(projects_columns - 2), attribute)

    projects_window.refresh()
