from views.main_view import main
import os
import json

# Load configuration
def get_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config
if __name__ == "__main__":
    main()
