"""Configuration handling
"""

import yaml

__config = None

def get_config():
    global __config
    if __config is None:
      with open("config.yaml", 'r') as stream:
          __config = yaml.load(stream)
    return __config
