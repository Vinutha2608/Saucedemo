import configparser
import os

config = configparser.ConfigParser()
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.ini")
config.read(file_path)

def get_config(key):
    if key == "url":
        # In CI reads from GitHub Secret, locally reads from config.ini
        return os.getenv("SAUCE_URL", config['DEFAULT'][key])
    return config['DEFAULT'][key]