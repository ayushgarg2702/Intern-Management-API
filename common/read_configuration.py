import configparser
import os
import json


# Read Config File
def read_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini'))
    return config