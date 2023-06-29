import json
import os

def save():
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def refresh():
    try:
        with open(path, 'r') as file:
            config = json.load(file)
        if isinstance(config, dict):
            return config
        print(' [conf warning] config.json is not a dict, use default!')
        return {}
    except (FileNotFoundError, json.JSONDecodeError):
        print(' [conf warning] config.json missing or unreadable, use default!')
        return {}

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

data = refresh()

get = data.get