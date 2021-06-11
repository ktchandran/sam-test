

import configparser
import json

def configToDict(config):
    result = {}
    for section in config.sections():
        config[section.lower()] = config[section]
        for key, value in config[section.lower()].items():
            try:
                result[key] = json.loads(value)
            except json.decoder.JSONDecodeError:
                raise Exception(f"Invalid json config value: {value}")
    return result

config = configparser.RawConfigParser()
# config.optionxform = lambda option: option

config.read('baseconfig.cfg')

values = configToDict(config)
print(values)