import configparser
import os

config = configparser.ConfigParser()

# Get full path of config file
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.ini")

config.read(file_path)

def get_config(key):
    return config['DEFAULT'][key]