import json


class Data:
    @staticmethod
    def load(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save(path, data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
