import os
import re
import time
from datetime import datetime
from stat import ST_MTIME
from photo_workflow import exif
from photo_workflow.utils.logging_photo import logger
from photo_workflow.helpers import conf

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
        date = exif.get_exif_data(exif_data, "Exif.Photo.DateTimeOriginal")
        date_pattern = '%Y-%m-%d_%H-%M-%S'
        if date is None:
            date = time.strftime(date_pattern, time.localtime(os.stat(self.full_path)[ST_MTIME]))
        else:
            date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S').strftime(date_pattern)

        return date

    def get_model(self, exif_data):
        """ Return camera model from exif data"""
        model = exif.get_exif_data(exif_data, "Exif.Image.Model")
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
        
    def __str__(self):
        return "Photo : {0}".format(self.full_path)