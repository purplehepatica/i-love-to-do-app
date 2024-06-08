import curses


# create_projects_window() itp
def display_projects(main_window: "curses.window", projects, current_project):
    main_window.refresh()

    curses.curs_set(0)
    main_window.keypad(True)
    curses.noecho()

    first_line = 0

    projects_lines = curses.LINES - 5
    projects_columns = curses.COLS

    projects_start_y = first_line
    projects_start_x = 0

    projects_window = curses.newwin(
        projects_lines, projects_columns, projects_start_y, projects_start_x
    )

    projects_window.border()

    projects_window.addstr(2, 1, "--- LISTA PROJEKTÓW ---".center(projects_columns - 2))

    for i, project_name in enumerate(projects):
        if i == current_project:
            projects_window.addstr(4 + i, 1, f"{i + 1}. {project_name}".center(projects_columns - 2), curses.A_REVERSE)
        else:
            projects_window.addstr(4 + i, 1, f"{i + 1}. {project_name}".center(projects_columns - 2))

    projects_window.refresh()
    main_window.refresh()
