"""
Define the the process for all our commands
"""
from abc import ABC, abstractmethod
from photo_workflow.photo_collection import PhotoCollectionFactory
from photo_workflow.utils.logging_photo import logger

def get_collection(collection_name):
    """
    Returns collections
    If parameter 'collection_name' is empty, returns all collections
    """
    if collection_name is not None:
        return PhotoCollectionFactory().get_collection(collection_name)

    return PhotoCollectionFactory().get_all_collections()

class AbstractProcess(ABC):

    @abstractmethod
    def is_enable(self, collection):
        pass

    @abstractmethod
    def process(self, photo, collection, force= False):
        pass

    @abstractmethod
    def update_metadata_file(self, collection):
        pass

    def run(self, collection_name, force=False):
        logger.debug("Start Process for %s", collection_name)
        collections = get_collection(collection_name)

        for collection in collections:
            if self.is_enable(collection):
                logger.info("Retrieving photos from collection %s", collection.name)
                for photo in collection.get_collection_files():
                    logger.debug("Current Photo file %s", photo.full_path)
                    try:
                        self.process(photo, collection, force)
                    except AttributeError as err:
                        logger.error("Cannot process file %s - error %s", photo.full_path, err)

                self.update_metadata_file(collection)


class TagProcess(AbstractProcess):

    def is_enable(self, collection):
        return collection.is_tag_enabled()

    def process(self, photo, collection, force=False):
        photo.tag(collection.metadata.content['tags'], force)

    def update_metadata_file(self, collection):
        collection.update_tag_info()


class RenameProcess(AbstractProcess):

    def is_enable(self, collection):
        return collection.is_rename_enabled()

    def process(self, photo, collection, force=False):
        photo.rename(force)

    def update_metadata_file(self, collection):
        collection.update_rename_info()


class SyncProcess(AbstractProcess):

    def is_enable(self, collection):
        return collection.is_sync_enabled()

    def process(self, photo, collection, force=False):
        # get related collection
        related_collection = collection.get_related_collection()
        related_photos = []

        for related_collec in related_collection:
            related_photos.extend(related_collec.get_collection_files())

        photo.sync(related_photos, collection.metadata)

    def update_metadata_file(self, collection):
        collection.update_sync_info()


class InitCollection():
    """ This class init a photo collection

    It creates a yaml file named 'metadata.yaml' with default structure into each folder
    This file contains those information :
    - Collection name
    - Creation date
    - Checksum
    - tags to apply to this collection


    This module works with several parameters
    - collection : create this file into specific collection.
                If no collection specified, loop on all collection
    - force : if true, backup and delete original metadata file
    """

    def __init__(self, collection_name, force):
        self.collection_name = collection_name
        self.force = force


    def process(self):
        logger.info('Init Collection Process - collection %s, force flag %s', self.collection_name, self.force)
        collections = get_collection(self.collection_name)

        for item in collections:
            logger.debug('Processing collection : %s', item)
            item.generate_metadata_file(self.force)
