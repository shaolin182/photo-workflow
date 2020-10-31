"""
Contains all logic for importing images files
"""
import os
from photo_workflow.helpers import conf, create_folder

def process(source, collection, type, recursive, filter, verbose):
    create_collection_folder(collection, verbose)


def copy_images():
    """
    Create collection folder on RAW and JPG directory
    Copy files from source directory into target directory
    """
    pass

def create_collection_folder(collection, verbose):
    """ Create collection folder both on RAW and JPG directory """
    create_folder(conf["raw_dir"] + collection, verbose)
    create_folder(conf["jpg_dir"] + collection, verbose)

def import_to_darktable():
    """
    Import images to darktable software
    Create preset for filtering on new collection
    """
    pass


def import_to_digikam():
    """
    Import images to digikam software
    """
    pass

create_collection_folder("test")