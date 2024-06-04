def input_project_name():
    return input("Jak nazwiesz swój nowy projekt?: ")

def input_project_index():
    return input("Projekt, o jakim ID chcesz usunąć?: ")

def get_project_names(data):
    return [project["name"] for project in data["projects"]]


def create_project_entry(project_name):
    return {
        'name': project_name
    }


def add_project(data, project_entry):
    data["projects"].append(project_entry)


def delete_project(data, project_index):
    data["projects"].pop(project_index)


def init_project_creation(data):
    project_name = input_project_name()
    project_entry = create_project_entry(project_name)

    add_project(data, project_entry)


def init_project_removal(data):
    project_index = int(input_project_index())
    delete_project(data, project_index)