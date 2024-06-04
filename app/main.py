from features.screen import Screen
from features.project import get_project_names, init_project_creation
from features.inputs import get_user_choice
from data.data import get_data, save_data


def main():
    data_path = "data/data.json"
    data = get_data(data_path)
    screen = Screen()

    while True:
        screen.display(get_project_names(data))
        user_choice = get_user_choice()

        match user_choice:
            case "p":
                # by może nie bazować na takich niejawnych formach data,
                # a raczej: load_data (from json) i save_data (to json)
                init_project_creation(data)
            case "w":
                quit()
            case "z":
                save_data(data_path, data)
            case _:
                pass


if __name__ == "__main__":
    main()
