def input_project_name():
    return input("Jak nazwiesz swój nowy projekt?: ")


def get_project_names(data):
    return [project["name"] for project in data["projects"]]


def create_project_entry(project_name):
    return {
        'name': project_name
    }


def add_project(data, project_entry):
    data["projects"].append(project_entry)


def init_project_creation(data):
    project_name = input_project_name()
    project_entry = create_project_entry(project_name)

    add_project(data, project_entry)