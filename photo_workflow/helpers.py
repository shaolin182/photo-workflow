import os
import yaml
import re

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


def load_tag_configuration():
    """ Load YAML configuration file into dict """
    return yaml.safe_load(open('conf_xmp_tag.yml'))


def list_files(basedir, recursive=False, pattern_to_exclude=None, verbose=False):
    """
    Return a list of files given some parameter

    @param : 
    - basedir : base directory where we looking for some files
    - recursive : does we look into sub directories
    - pattern_to_exclude : a regex for excluding some files
    """

    list_files = []

    # List files of a specific source
    if recursive:
        for dirpath, dirname, files in os.walk(basedir):
            for file in files:
                list_files.append("{0}/{1}".format(dirpath, file))
                #rename_file(dirpath, file, suffix, exclude, verbose)
    else:
        for file in os.listdir(basedir):
            full_path = "{0}/{1}".format(basedir, file)
            if os.path.isfile(full_path):
                list_files.append(full_path)
                #rename_file(source, file, suffix, exclude, verbose)

    # Exclude result that matches a pattern
    result = []
    if pattern_to_exclude:
        for a_file in list_files:
            if re.search(pattern_to_exclude, a_file, re.IGNORECASE) is not None:
                result.append(a_file)
                if verbose:
                    print("File {0} - Match exlusion request {1}".format(a_file, pattern_to_exclude))
    else:
        result = list_files

    
    return result

conf = load_configuration()
conf_tag = load_tag_configuration()