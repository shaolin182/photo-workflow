"""
Contains all logic for renaming images files
"""
import os
import os.path
import time
import re
from stat import *
import piexif
from datetime import datetime
import photo_workflow.exif

def rename(source, suffix, recursive, exclude, verbose):
    """ 
    Loop on source directory and call rename process for all matching files

    @param:
    - source : source directory
    - suffix : suffix to applied to all filenames
    - recursive : find files recursively or not
    - exclude : regex to exclude some files
    - verbose : add debug log if true
    """

    if verbose:
        print("Recursive mode : {0}".format(recursive))

    if recursive:
        for dirpath, dirname, files in os.walk(source):
            for file in files:
                rename_file(dirpath, file, suffix, exclude, verbose)
    else:
        for file in os.listdir(source):
            full_path = "{0}/{1}".format(source, file)
            if os.path.isfile(full_path):
                rename_file(source, file, suffix, exclude, verbose)


def rename_file(directory, file, suffix, exclude, verbose):
    """ 
    Rename a file

    @param:
    - directory : source directory
    - file : current file
    - suffix : suffix to applied to file
    - exclude : regex to exclude some files
    - verbose : add debug log if true
    """
    filename, extension = os.path.splitext(file)
    if extension.lower() not in [".jpg", ".jpeg", ".nef"]:
        if verbose:
            print("File {0} - Extension {1} is not handled".format(filename, extension))
        return

    if exclude and re.search(exclude, filename, re.IGNORECASE) is not None:
        if verbose:
            print("File {0} - Match exlusion request {1}".format(filename, exclude))
        return

    source = directory + "/" + file
    date_from_file = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(os.stat(source)[ST_MTIME]))
    data = exif.load_exif_data(source)
    original_date = exif.get_exif_data(data, piexif.ExifIFD.DateTimeOriginal)
    if original_date is not None:
        target = build_new_filename(directory, file, suffix, original_date)
        os.rename(source, target)
        if verbose:
            print("File {0} - renamed in {1}".format(source, target))
    else:
        target = build_new_filename(directory, file, suffix, date_from_file, True)
        os.rename(source, target)
        if verbose:
            print("File {0} - renamed in {1}".format(source, target))

def build_new_filename(directory, file, suffix, exif_date, date_as_string=False, index=0):
    """
    Build filename of the targeted file

    @param:
    - directory : source directory
    - file : current file
    - suffix : suffix to applied to file
    - exif_date : data used for building filename
    """
    if date_as_string is False:
        date = datetime.strptime(str(exif_date, 'utf-8'), '%Y:%m:%d %H:%M:%S')
        filename = date.strftime("%Y-%m-%d_%H-%M-%S")
    else :
        filename = exif_date
    filename_data, extension = os.path.splitext(file)

    if suffix is None and index == 0:
        format = "{directory}/{filename}{extension}"
    elif suffix is None:
        format = "{directory}/{filename}_{index}{extension}"
    elif index == 0:
        format = "{directory}/{filename}_{suffix}{extension}"
    else:
        format = "{directory}/{filename}_{index}_{suffix}{extension}"

    target_filename = format.format(directory=directory, suffix=suffix,
                                    filename=filename, extension=extension, index=index)

    if os.path.isfile(target_filename):
        index += 1
        target_filename = build_new_filename(directory, file, suffix, exif_date, date_as_string, index)

    return target_filename