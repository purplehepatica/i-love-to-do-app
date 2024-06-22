class Project:
    def __init__(self, project_name, tasks=[]):
        self.name = project_name
        self.tasks = tasks

    @property
    def task_names(self):
        return [task.name for task in self.tasks]

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_index):
        self.tasks.pop(task_index)

    def get_task(self, task_index):
        return self.tasks[task_index]

    def serialize(self):
        return {
            "name": self.name,
            "tasks": [task.__dict__ for task in self.tasks]
        }