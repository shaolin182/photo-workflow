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


class PhotoCollectionMetadata:

    def __init__(self, collection_path, collection_name):
        self.collection_path = collection_path
        self.collection_name = collection_name
        self.filename = os.path.join(self.collection_path, 'metadata.yaml')
        self.content = self.get_content()

    def is_metadata_exist(self):
        """ Return true if metadata file already exists """
        return os.path.exists(os.path.join(self.filename))

    def get_content(self):
        if self.is_metadata_exist():
            return self.load_content_file()
        else:
            return self.init()

    def load_content_file(self):
        """ Load metadata file """
        with open(self.filename, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

    def write(self):
        """ Write metadata file """
        with open(self.filename, 'w') as yaml_file:
            yaml.dump(self.content, yaml_file,  allow_unicode=True)
            logger.info('Collection %s Metadata file created %s', self.collection_name, self.filename)

    def update(self):
        """ Merge existing files with default content"""
        default_content = self.init()
        self.content = {**default_content, **self.content}

    def backup(self):
        """Backup metadata file"""
        now = datetime.now()
        backup_filename = 'metadata_{0}.yaml'.format(now.strftime("%Y%m%d_%H%M%S"))

        dest_file = os.path.join(self.collection_path, backup_filename)

        shutil.copyfile(self.filename, dest_file)
        logger.info('%s backuped to %s', self.filename, dest_file)

    def init(self):
        """ Generate metadata content"""
        now = datetime.now()

        return {
            'collection' : self.collection_name,
            'creation_date' : now.strftime("%Y/%m/%d %H:%M:%S"),
            'status': 'INIT',
            'tags' : {
                'enable': False,
                'last_tag_on' : None,
                'add' : [
                    {'name':'Xmp.lr.hierarchicalSubject', 'values': []},
                    {'name':'Xmp.dc.Subject', 'values': []}
                ],
                'remove' : [
                    {'name' : 'Xmp.lr.hierarchicalSubject', 'values' : []},
                    {'name' : 'Xmp.dc.Subject', 'values': []}
                ]
            },
            'rename' : {
                'last_rename_on' : None,
                'enable' : False
            },
            'sync' : {
                'enable' : False,
                'last' : None, 
                'include': [],
                'exclude': []
            },
            'rsync' : {
                'gdrive' : {
                    'enable': True,
                    'last': None
                },
                'nas' : {
                    'enable': True,
                    'last': None
                }
            }
        }

class PhotoCollection:
    """Represents a collection of photo """

    def __init__(self, name, conf, path):
        self.name = name
        self.conf = conf
        self.type_collection = conf["type"]
        self.path = path
        self.metadata = PhotoCollectionMetadata(self.path, self.name)

    def is_collection_path_exist(self):
        """ Return true if collection path exists """
        return os.path.exists(self.path)

    def is_rename_enabled(self):
        """ Return true if rename process is enabled"""
        return True if self.metadata.content["rename"]["enable"] else False

    def is_tag_enabled(self):
        """ Return true if tag process is enabled"""
        return True if self.metadata.content["tags"]["enable"] else False

    def is_sync_enabled(self):
        """ Return true if tag process is enabled"""
        return True if self.metadata.content["sync"]["enable"] else False

    def update_rename_info(self):
        now = datetime.now()
        self.metadata.content["rename"]["last_rename_on"] = now.strftime("%Y/%m/%d %H:%M:%S")
        self.metadata.write()

    def update_tag_info(self):
        now = datetime.now()
        self.metadata.content["tags"]["last_tag_on"] = now.strftime("%Y/%m/%d %H:%M:%S")
        self.metadata.write()

    def update_sync_info(self):
        now = datetime.now()
        self.metadata.content["sync"]["last"] = now.strftime("%Y/%m/%d %H:%M:%S")
        self.metadata.write()

    def generate_metadata_file(self, force):
        """
        Create a metadata file
        """
        if self.is_collection_path_exist() is False:
            logger.info('%s path does not exist, collection %s not created', self.path, self.name)
            return

        if self.metadata.is_metadata_exist():
            self.metadata.backup()
            self.metadata.update()
        
        self.metadata.write()

    
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

    def get_related_collection(self):
        """
        Get related collections
        A related collection is a collection with same name
        """
        all_collections = PhotoCollectionFactory().get_all_collections();
        return [collec for collec in all_collections if collec.name == self.name and collec.type_collection != self.type_collection]


    def __str__(self):
        return "Collection : {0} - {1} - {2}".format(self.name, self.type_collection, self.path)
