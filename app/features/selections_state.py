class SelectionsState:
    def __init__(self, current_menu_option: int = 0, current_project_position: int = 0):
        self.selected_menu_option: int = current_menu_option
        self.selected_project_position: int = current_project_position
