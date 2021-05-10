"""
PhotoCollection class
"""
import os
import re
from datetime import datetime
from glob import glob
import shutil
import yaml
from photo_workflow.photo import Photo
from photo_workflow.helpers import conf, get_collection_path, check_regex
from photo_workflow.utils.logging_photo import logger

def get_metadata_content_file(collection):
    """
    Generate metadata content
    """
    now = datetime.now()

    return {
        'collection' : collection,
        'creation_date' : now.strftime("%Y/%m/%d %H:%M:%S"),
        'status': 'INIT',
        'tags' : [],
        'rename' : {
            'last_rename_on' : None,
            'enable' : False
        }
    }

class PhotoCollectionFactory:
    """Some methods for building a PhotoCollection object"""

    def get_collection(self, collection_name):
        """ Return collections by name """

        check_regex(conf['regex']['collection'], collection_name)

        collections = []

        for item in conf["collections"]:
            collection_path = get_collection_path(item["basePath"], collection_name)
            if os.path.isdir(collection_path):
                collections.append(PhotoCollection(collection_name, item, collection_path))

        return collections

    def get_all_collections(self):
        """Return all collections"""
        collections = []

        for item in conf["collections"]:
            for collection in glob(item["collectionPath"]):
                name = os.path.basename(os.path.normpath(collection))
                collections.append(PhotoCollection(name, item, collection))

        return collections


class PhotoCollection:
    """Represents a collection of photo """

    def __init__(self, name, conf, path):
        self.name = name
        self.conf = conf
        self.type_collection = conf["type"]
        self.path = path
        self.metadata = self.load_metadata_file()

    def load_metadata_file(self):
        """ Load metadata file """
        metadata_file = os.path.join(self.path, 'metadata.yaml')
        with open(metadata_file, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

    def is_metadata_exist(self):
        """
        Return true if metadata file already exists
        """
        return os.path.exists(os.path.join(self.path, 'metadata.yaml'))


    def is_collection_path_exist(self):
        """
        Return true if collection path exists
        """
        return os.path.exists(self.path)


    def is_rename_enabled(self):
        """ Return true if rename process is enabled"""
        if self.metadata["rename"]["enable"] is True:
            return True
        else:
            return False


    def update_rename_info(self):
        now = datetime.now()
        self.metadata["rename"]["last_rename_on"] = now.strftime("%Y/%m/%d %H:%M:%S")
        self.write_metadata_file()


    def backup_metadata_file(self):
        """Backup metadata file"""
        now = datetime.now()
        backup_filename = 'metadata_{0}.yaml'.format(now.strftime("%Y%m%d_%H%M%S"))

        original_file = os.path.join(self.path, 'metadata.yaml')
        dest_file = os.path.join(self.path, backup_filename)

        shutil.copyfile(original_file, dest_file)
        logger.info('%s backuped to %s', original_file, dest_file)


    def generate_metadata_file(self, force):
        """
        Create a metadata file
        """
        if self.is_collection_path_exist() is False:
            logger.info('%s path does not exist, collection %s not created', self.path, self.name)
            return

        if self.is_metadata_exist() and force is False:
            # Log Stop treatment for that collection
            logger.info('Collection %s Metadata file already exists', self.name)
            return
        elif self.is_metadata_exist():
            # Backup existing file
            self.backup_metadata_file()

        self.metadata = get_metadata_content_file(self.name)
        self.write_metadata_file()

    def write_metadata_file(self):
        metadata_file = os.path.join(self.path, 'metadata.yaml')
        with open(metadata_file, 'w') as yaml_file:
            yaml.dump(self.metadata, yaml_file,  allow_unicode=True)
            logger.info('Collection %s Metadata file created %s', self.name, metadata_file)

    def get_collection_files(self):
        """
        Return the file list of that collection
        It list all files on current directory recursively
        Then, it filters files according to configuration
        """

        include_file_regex = '|'.join(self.conf["include"])
        exclude_file_regex = '|'.join(self.conf["exclude"])

        include = re.compile(include_file_regex, re.IGNORECASE)
        exclude = re.compile(exclude_file_regex, re.IGNORECASE)

        files = glob(self.path + '/**/*', recursive=True)
        return [Photo(f) for f in files if include.match(f) and exclude.match(f) is None]

    def __str__(self):
        return "Collection : {0} - {1} - {2}".format(self.name, self.type_collection, self.path)
