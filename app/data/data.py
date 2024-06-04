import json


def get_data(path):
    with open(path, "r", encoding="utf-8") as data:
        return json.load(data)


def save_data(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
