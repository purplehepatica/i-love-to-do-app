import json


class Data:
    def __init__(self, path):
        self.path = path
        self.data = {}

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
