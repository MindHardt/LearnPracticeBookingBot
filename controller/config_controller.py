import json


def read_json() -> dict:
    with open('config.json') as f:
        return json.load(f)


__config = read_json()


def set_value(config, value):
    """Sets configuration value to specified and returns previous value. If they key doesn't exists then None is returned."""
    current_value = __config.pop(config, None)
    if current_value is not None:
        __config[config] = value
    save_json()
    return current_value


def get_value(config):
    """Gets config related to specified key, or None if it doesn't exist"""
    return __config.get(config, None)


def save_json():
    with open('config.json', 'w') as f:
        json.dump(__config, f)


def get_config() -> str:
    return str(__config)
