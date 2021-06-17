import yaml

# A very basic 'library' to help manage reading from and writing to the config.yaml file used during execution.
def open_yaml():
    configs = open('config.yaml', 'r')
    keys = yaml.safe_load(configs)
    return keys

def get_yaml_value(key):
    keys = open_yaml()
    return keys[key]

def set_yaml_value(key, value):
    keys = open_yaml()
    keys[key] = value
    configs = open('config.yaml', 'w')
    yaml.dump(keys, configs)