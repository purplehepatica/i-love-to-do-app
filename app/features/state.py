class State:
    def __init__(self, current_menu_option=0, current_project_position=0):
        self.selected_menu_option = current_menu_option
        self.selected_project_position = current_project_position

    def increase_selected_menu_option(self):
        self.selected_menu_option += 1

    def decrease_selected_menu_option(self):
        self.selected_menu_option -= 1

    def increase_selected_project_position(self):
        self.selected_project_position += 1

    def decrease_selected_project_position(self):
        self.selected_project_position -= 1
