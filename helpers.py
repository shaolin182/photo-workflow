import os
import yaml

def create_folder(dir_name, verbose):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        if verbose:
            print("Directory " , dir_name ,  " Created")
    else:
        if verbose:
            print("Directory " , dir_name ,  " already exists")


def load_configuration():
    """ Load YAML configuration file into dict """
    return yaml.safe_load(open('conf.yml'))

conf = load_configuration()