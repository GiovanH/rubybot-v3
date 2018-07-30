import json


def load(filename):
    with open("jobj/" + filename + ".json", 'r') as file:
        return json.load(file)


def save(object, filename):
    j = json.dumps
    with open("jobj/" + filename + ".json", 'w') as file:
        j = json.dump(object, file, indent=4)
