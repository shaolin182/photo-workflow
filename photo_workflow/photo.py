import os
import re
import time
from collections import Counter
from datetime import datetime
from shutil import copyfile
from stat import ST_MTIME
from photo_workflow import exif
from photo_workflow.utils.logging_photo import logger
from photo_workflow.helpers import conf

class ExifData:
    pass

class Photo:
    """
    Represents a photo
    """

    def __init__(self, full_path):
        self.full_path = full_path
        self.path = os.path.dirname(full_path)
        self.filename, self.extension = os.path.splitext(os.path.basename(full_path))

    def rename(self, force=False):
        """ Rename a file according to its exif data"""

        logger.info("Start process for renaming photo %s", self.full_path)
        # Check if we continue on rename processing
        regex = re.compile(conf["regex"]["photo_file"], re.IGNORECASE)
        if force is False and regex.match(self.filename):
            logger.debug("File %s not renamed as it matches expected regex", self.full_path)
            return

        # Get exif data
        data = exif.load_exif_data(self.full_path)
        original_date = self.get_date(data)
        model = self.get_model(data)

        # Build new filename
        new_filename = self.build_filename(original_date, model)

        # Rename
        if self.full_path != new_filename:
            os.rename(self.full_path, new_filename)
            logger.info("Rename photo %s into %s", self.full_path, new_filename)
        else:
            logger.debug("File %s has not been renamed", self.full_path)


    def get_date(self, exif_data):
        """
        Return original date of the photo from exif data
        If the exif data does not exist, return filesystem date
        """
        date = exif.get_exif_data(exif_data, "Exif.Photo.DateTimeOriginal")[0]
        date_pattern = '%Y-%m-%d_%H-%M-%S'
        if date is None:
            date = time.strftime(date_pattern, time.localtime(os.stat(self.full_path)[ST_MTIME]))
        else:
            date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S').strftime(date_pattern)

        return date

    def get_model(self, exif_data):
        """ Return camera model from exif data"""
        model = exif.get_exif_data(exif_data, "Exif.Image.Model")[0]
        if model:
            return model.replace(' ', '_')

        return None

    def build_filename(self, date, model, index=0):
        """ Build a filename from date, model and index """
        new_filename = '_'.join(str(e) for e in filter(None, [date, index, model]))
        new_filename = os.path.join(self.path, new_filename + self.extension)

        # Filename already exists, add index
        logger.debug("New Filename - %s ", new_filename)
        if new_filename != self.full_path and os.path.isfile(new_filename):
            logger.debug("Filename already exists - %s ", new_filename)
            index += 1
            new_filename = self.build_filename(date, model, index)

        return new_filename

    def tag(self, tags, force=False):
        """Apply Exif Data from metadata file"""
        logger.info("Start process for tagging photo %s", self.full_path)
        data = exif.load_exif_data(self.full_path)

        # Extract tags to apply from conf
        remove_tags = tags["remove"]
        add_tags = tags["add"]

        # Remove tags
        for remove_tag in remove_tags:
            exif_values = exif.get_exif_data(data, remove_tag['name'])
            # Remove from existing list, values from configuration
            exif_values = [] if exif_values is None else exif_values
            new_values = list((exif for exif in exif_values if exif not in remove_tag['values']))

            if new_values is None or len(new_values) == 0:
                # delete tag
                logger.debug("Remove tag %s on file %s", new_values, self.full_path)
                exif.remove_exif_data(data, remove_tag["name"])

            elif Counter(exif_values) != Counter(new_values):
                # update tag data
                logger.debug("Apply those tags %s on file %s", new_values, self.full_path)
                exif.add_or_update_exif_data(data, remove_tag["name"], new_values)


        # Add tags
        for add_tag in add_tags:
            exif_values = exif.get_exif_data(data, add_tag['name'])
            logger.debug("existing tags %s with values %s", add_tag['name'], exif_values)
            exif_values = [] if exif_values is None else exif_values
            # Add new values from conf into existing list, without duplicates
            new_values = list(exif_values)
            new_values.extend((x for x in add_tag['values'] if x not in new_values))

            if Counter(exif_values) != Counter(new_values):
                # update tag data
                logger.debug("Apply those tags %s on file %s", new_values, self.full_path)
                exif.add_or_update_exif_data(data, add_tag["name"], new_values)

        exif.write_exif_data(data)

    def sync(self, related_collection_files, metadata):
        """
        Check if current file exist in related collection

        If it's not found, then move it to a trash folder
        Otherwise, keep it
        """

        include_file_regex = '|'.join(metadata.content["sync"]["include"])
        exclude_file_regex = '|'.join(metadata.content["sync"]["exclude"])

        include = re.compile(include_file_regex, re.IGNORECASE)
        exclude = re.compile(exclude_file_regex, re.IGNORECASE)

        if include.match(self.filename) and exclude.match(self.filename) is None:
            # Build list of filenames from current filename
            filenames_list = self.build_filename_list(self.filename)

            found = False
            # If none of those filenames are found  in related collections, delete it
            for filename in filenames_list: 
                for related_file in related_collection_files:
                    if related_file.filename == filename:
                        found = True

            if found is False:
                # Move it to temp directpry
                logger.debug("Move file %s to temp directory", self.full_path)
                os.makedirs(os.path.join(conf["tmp_dir"], metadata.content["collection"]), exist_ok=True)
                copyfile(self.full_path, os.path.join(conf["tmp_dir"], metadata.content["collection"], self.filename + self.extension))
                os.remove(self.full_path)
        else:
            logger.info("File %s not sync as it does not match configuration", self.filename)


    def build_filename_list(self, filename, filename_list=None, separator="_"):

        print("Current filename : {0} - Current list files : {1}".format(filename, filename_list))

        regex_filename_date = r"\d{4}-\d{2}-\d{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}$"
        regex_filename_date_index = r"\d{4}-\d{2}-\d{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}_[0-9]{1}$"

        filename_without_ext = os.path.splitext(filename)[0]
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
                self.build_filename_list("{0}{1}".format(left_filename, extension), filename_list, separator)

        return filename_list

    def __str__(self):
        return "Photo : {0}".format(self.full_path)
