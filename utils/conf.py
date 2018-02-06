import os
import json


def conf_exists():
    """Checks if configuration exists"""
    return os.path.isfile("conf.json")


def update_conf(conf):
    """Update configuration"""
    f = open("conf.json", 'w')
    f.write(json.dumps(conf, indent=4))
    f.close()


def get_conf():
    """Reads the config file and deserialises it"""
    return json.loads(open("conf.json", 'r').read())
