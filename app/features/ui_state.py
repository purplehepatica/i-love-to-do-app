class UIState:
    def __init__(
            self,
            menu_option: int = 0,
            project_position: int = 0,
            project_task_position: int = 0,
            view_type: str = "project",
            mode: str = "normal"
    ):
        self.menu_position: int = menu_option
        self.project_position: int = project_position
        self.project_task_position: int = project_task_position
        self.view_type = view_type
        self.mode = mode

    @classmethod
    def from_dict(cls, ui_state_dict):
        return cls(
            menu_option=ui_state_dict.get("menu_position", 0),
            project_position=ui_state_dict.get("project_position", 0),
            project_task_position=ui_state_dict.get("project_task_position"),
            view_type=ui_state_dict.get("view_type", "project"),
            mode=ui_state_dict.get("mode", "normal")
        )

    def serialize(self):
        return {
            "ui_state": self.__dict__
        }
