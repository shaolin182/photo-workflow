'''
This module init a photo collection

It creates a yaml file named 'metadata.yaml' with default structure into each folder
This file contains those information :
- Collection name
- Creation date
- Checksum
- tags to apply to this collection


This module works with several parameters
- collection : create this file into specific collection.HEll
               If no collection specified, loop on all collection
- force : if true, backup and delet original metadata file

'''
from photo_workflow.photo_collection import PhotoCollectionFactory
from photo_workflow.utils.logging_photo import logger

def main(collection_name=None, force=False):
    """
    Determine collections to process
    """
    logger.info('Init Collection Process - collection %s, force flag %s', collection_name, force)

    if collection_name is not None:
        collections = PhotoCollectionFactory().get_collection(collection_name)
    else:
        collections = PhotoCollectionFactory().get_all_collections()

    for item in collections:
        logger.debug('Processing collection : %s', item)
        item.generate_metadata_file(force)
