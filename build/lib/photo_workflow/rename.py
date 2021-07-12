"""
Contains all logic for renaming images files
"""
from photo_workflow.photo_collection import PhotoCollectionFactory
from photo_workflow.utils.logging_photo import logger

def rename_process(collection_name, force=False):
    """
    Launch rename process on a particular collection
    or on all collections
    Rename process is run only if it has been activated in metadata collection file
    """
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
                except AttributeError as err:
                    logger.error("Cannot rename file %s - error %s", photo.full_path, err)

            collection.update_rename_info()
