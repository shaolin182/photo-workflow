"""
Contains all logic for synchronizing RAW folders and JPG folders
If RAW file has been deleted, matching JPG files should also be deleted
If JPG file has been deleted, matching RAW files should also be deleted
"""
import os
import re
from shutil import copyfile
from photo_workflow.helpers import conf

def sync(collection, source, custom_filter, verbose, recursive=True):
    """
    Sync collection photos between RAW datasource and JPG datasource

    If source is RAW, for each JPG files we look for RAW matching files. If no file exist, then we delete the JPG file
    If source is JPG, for each RAW files we look for JPG matching files. If no file exist, then we delete the RAW file
    """
    # Build RAW file list and JPG file list
    jpg_file_list = build_file_dict(conf["jpg"], collection, custom_filter)
    raw_file_list = build_file_dict(conf["raw"], collection, custom_filter)

    if source == "RAW":
        sync_files(raw_file_list, jpg_file_list)
    else:
        sync_files(jpg_file_list, raw_file_list)


def sync_files(source_file_list, target_file_list):
    for key in target_file_list.keys():
        print("Processing file : {0} | {1}".format(key, target_file_list[key]["filename"]))

        # As a photo can have multiple instances (different photo treatment for example) with different names
        # Example : 2020-12-26_13-46-36_D750.JPG, 2020-12-26_13-46-36_D750_darktable.JPG, 2020-12-26_13-46-36_D750_darktable_01.JPG
        # we do not want that photos with different suffixes to be deleted by process
        # So for a same key, we found some common name

        if file_exist_in_list(source_file_list, build_filename_list(key)) is False:
            # If no reference is found, delete file
            copyfile(target_file_list[key]["full_path"], conf["tmp_dir"] + target_file_list[key]["filename"])
            os.remove(target_file_list[key]["full_path"])
            print("delete file {0}".format(target_file_list[key]["full_path"]))
        else:
            print("Found file {0}".format(target_file_list[key]["full_path"]))


def get_directory_path(conf_sync, collection):
    """
    Build directory where images files are saved given a collection name
    and application conf
    """

    year = extract_year_from_collection(collection)
    return conf_sync["dir"] + year + "/" + collection


def file_exist_in_list(file_list, filename_list):

    for filename in filename_list:
        if file_list.get(filename) is not None:
            return True

    return False


def build_filename_list(filename, filename_list=None, separator="_"):

    print("Current filename : {0} - Current list files : {1}".format(filename, filename_list))

    regex_filename_date = r"\d{4}-\d{2}-\d{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}$"
    regex_filename_date_index = r"\d{4}-\d{2}-\d{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}_[0-9]{1}$"

    filename_without_ext = os.path.splitext(filename)[0]
    print("Filename without extension : {0}".format(filename_without_ext))
    extension = os.path.splitext(filename)[1]

    if filename_list is None:
        filename_list = []

    if re.search(regex_filename_date, filename_without_ext) or re.search(regex_filename_date_index, filename_without_ext):
        # filename match regex, then return only filename
        filename_list.append(filename)
    else:
        # split filename with default separator
        left_filename = filename_without_ext.rpartition(separator)[0]
        filename_list.append(filename)
        if left_filename != '':
            build_filename_list("{0}{1}".format(left_filename, extension), filename_list, separator)



    return filename_list


def build_file_dict(conf, collection, custom_filter):

    current_dir = get_directory_path(conf, collection)
    res = {}

    if (custom_filter is not None):
        conf["include"].append(custom_filter)

    print(conf["include"])
    for dirpath, dirname, files in os.walk(current_dir):
        for file in files:
            print("Processing file : " + file)
            if all(re.search(regex, file, re.IGNORECASE) for regex in conf["include"]):
                print("Include : OK")
                if any(re.search(regex, file, re.IGNORECASE) for regex in conf["exclude"]) is False:
                    print("Exclude : OK")
                    key = filename_without_extension(file)
                    res[key] = {
                        "full_path": dirpath + "/" + file,
                        "filename": file
                    }

    return res


def filename_without_extension(full_filename):
    return os.path.splitext(full_filename)[0]


def extract_year_from_collection(collection):
    return collection[:4]
