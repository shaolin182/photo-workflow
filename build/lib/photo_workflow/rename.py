"""
Contains all logic for renaming images files
"""
import os
import os.path
import time
import re
from stat import *
from datetime import datetime 
from photo_workflow import exif
from photo_workflow.photo_collection import PhotoCollectionFactory
from photo_workflow.utils.logging_photo import logger

def rename_process(collection_name, force=False):

    logger.info("Renaming photos from collection %s", collection_name)

    collections = []

    if collection_name is not None:
        collections = PhotoCollectionFactory().get_collection(collection_name)
    else:
        collections = PhotoCollectionFactory().get_all_collections()

    for collection in collections:
        if collection.is_rename_enabled():
            logger.debug("Retrieving photos from collection %s", collection.name)
            for photo in collection.get_collection_files():
                try:
                    photo.rename(force)
                except AttributeError as e:
                    logger.error("Cannot rename file %s - error %s", photo.full_path, e)
            
            collection.update_rename_info()


def build_filename(a_file, exif_data, index=0):

    # Get Date from exif
    file_date = exif.get_exif_data(exif_data, "Exif.Photo.DateTimeOriginal")
    if file_date is None:
        # Log error, use file system date
        file_date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(os.stat(a_file)[ST_MTIME]))

    # Get model from exif
    model = exif.get_exif_data(exif_data, "Exif.Image.Model")

    filename = '_'.join(str(e) for e in filter(None, [file_date, model, index]))

    # Filename already exists, add index
    if os.path.isfile(filename):
        index += 1
        filename = build_filename(a_file, exif_data, index)

    return filename

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
    original_date = get_original_date(data, file)
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

def get_original_date(exif_data, file):
    """
    As filename are build with date time, we look into exif data for original date
    Original date can be present in tag 'Exif.Photo.DateTimeOriginal' for RAW files and in 'DateTimeOriginal' for JPG files

    If original date is not found, raise an error
    """
    original_date = exif.get_exif_data(exif_data, "Exif.Photo.DateTimeOriginal")
    if original_date is None:
        original_date = exif.get_exif_data(exif_data, "DateTimeOriginal")

    if original_date is None:
        print('No date found in file {0}'.format(file))

    return original_date

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
        date = datetime.strptime(exif_date, '%Y:%m:%d %H:%M:%S')
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