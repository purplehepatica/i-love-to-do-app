class UIState:
    def __init__(
            self,
            menu_option: int = 0,
            project_position: int = 0,
            project_task_position: int = 0,
            view_type: str = "project",
            mode: str = "normal"
    ):
        self.menu: int = menu_option
        self.project: int = project_position
        self.project_task: int = project_task_position
        self.view_type = view_type
        self.mode = mode

    @classmethod
    def from_dict(cls, ui_state_dict):
        return cls(
            menu_option=ui_state_dict.get("menu", 0),
            project_position=ui_state_dict.get("project", 0),
            project_task_position=ui_state_dict.get("project_task"),
            view_type=ui_state_dict.get("view_type", "project"),
            mode=ui_state_dict.get("mode", "normal")
        )

    def serialize(self):
        return {
            "selected_positions": self.__dict__
        }

    """
        ui_state.project = data["ui_state"]["project"]
    ui_state.menu = data["ui_state"]["menu"]
    ui_state.view_type = data["ui_state"]["view_type"]
    ui_state.mode = data["ui_state"]["mode"]
    """