import json

def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
