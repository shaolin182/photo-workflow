import os
import re
import pkg_resources
import yaml
from photo_workflow.utils.logging_photo import logger

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
    conf_file = pkg_resources.resource_stream(__name__, "conf.yml")
    return yaml.safe_load(conf_file)


def load_tag_configuration():
    """ Load YAML configuration file into dict """
    conf_xmp_file = pkg_resources.resource_stream(__name__, "conf_xmp_tag.yml")
    return yaml.safe_load(conf_xmp_file)


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

def check_regex(pattern, string):
    """
    Check that a value is valid according a regex
    Throw an exception if an error occurs
    """
    result = re.search(pattern, string)
    if result is None:
        logger.error("'%s' does not match configured regex '%s'", string, pattern)
        raise ValueError("'{0}' does not match configured regex '{1}".format(string, pattern))


def get_collection_path(base_path, collection):
    """
    Build directory where images files are saved given a collection name
    and application conf
    """
    year = extract_year_from_collection(collection)
    return os.path.join(base_path, year, collection)


def get_directory_path(conf_sync, collection):
    """
    Build directory where images files are saved given a collection name
    and application conf
    """
    year = extract_year_from_collection(collection)
    return conf_sync["dir"] + year + "/" + collection


def extract_year_from_collection(collection):
    return collection[:4]

conf = load_configuration()
conf_tag = load_tag_configuration()
