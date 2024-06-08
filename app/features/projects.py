class Projects:
    def __init__(self, projects):
        self.projects = projects

    @property
    def names(self):
        return [project["name"] for project in self.projects]

    @staticmethod
    def create_project_entry(project_name):
        return {
            'name': project_name
        }

    def add(self, project_name):
        project_entry = self.create_project_entry(project_name)

        self.projects.append(project_entry)

    def delete(self, project_index):
        self.projects.pop(project_index)
