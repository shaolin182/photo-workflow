"""
Contains all logic for synchronizing RAW folders and JPG folders
If RAW file has been deleted, matching JPG files should also be deleted
If JPG file has been deleted, matching RAW files should also be deleted
"""
import os
import re
from photo_workflow.helpers import conf

def sync(collection, source, custom_filter, verbose, recursive=True):
    if source == "RAW":
        source_directory = conf["raw"]
        target_directory = conf["jpg"]
    else:
        source_directory = conf["jpg"]
        target_directory = conf["raw"]

    year = extract_year_from_collection(collection)
    source_directory["dir"] = source_directory["dir"] + year + "/" + collection
    target_directory["dir"] = target_directory["dir"] + year + "/" + collection

    target_file_list = build_file_dict(target_directory, custom_filter)
    source_file_list = build_file_dict(source_directory, custom_filter)

    # print("Source")
    # print(source_file_list)

    # print("target")
    # print(target_file_list)

    for key in target_file_list.keys():
        print("Processing file : {0} | {1}".format(key, target_file_list[key]["filename"]))
        if source_file_list.get(key) is None:
            os.rename(target_file_list[key]["full_path"], conf["tmp_dir"] + target_file_list[key]["filename"])
            print("delete file {0}".format(target_file_list[key]["full_path"]))
        else:
            print("Found file {0}".format(source_file_list[key]["full_path"]))


def build_file_dict(source, custom_filter):
    res = {}
    source["include"].append(custom_filter)
    print(source["include"])
    for dirpath, dirname, files in os.walk(source["dir"]):
        for file in files:
            print("Processing file : " + file)
            if all(re.search(regex, file, re.IGNORECASE) for regex in source["include"]):
                print("Include : OK")
                if any(re.search(regex, file, re.IGNORECASE) for regex in source["exclude"]) is False:
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


def find_files(source, filename, verbose):
    for dirpath, dirname, files in os.walk(source):
        for file in files:
            print("Current Target file {0} - file to found : {1}".format(file, filename))
            if re.search(filename, file, re.IGNORECASE) is not None:
                return True
    
    return False

