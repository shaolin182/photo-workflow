"""
Package for reading and writing exif tag on images
"""
from pyexiv2 import ImageMetadata
from photo_workflow.helpers import list_files, conf_tag

def tag_process(source, tag_name, tag_value, delimiter, remove=False, verbose=False):
    """
    Look for all files of the source directory and then applied operation on tag image
    Operation can be :
    - remove operation :  specific tag is removed from image
    - add operation : a tag is created or updated with new values

    @param
    - source : source directory
    - tag_name : tag to add or remove
    - tag value : value of the tag
    - delimiter : if tag can contain list then tag value is splitted using that delimiter
    - remove : True if we remove tag, false otherwise
    - verbose : add logs
    """
    files = list_files(source, False, None, verbose)

    for a_file in files:
        exif_data = load_exif_data(a_file)

        if remove:
            remove_exif_data(exif_data, tag_name)
            if verbose:
                print("Remove tag {0} on file {1}".format(tag_name, a_file))
        else:
            tag_to_add = []
            for tag in get_tag_list(tag_name, tag_value, delimiter):
                tag_to_add.append(tag)
                if verbose:
                    print("Add value {0} on tag {1} for file {2}".format(tag, tag_name, a_file))

            add_or_update_exif_data(exif_data, tag_name, tag_to_add)


def is_tag_list(tag_name, conf):
    """
    Return true if a XMP tag accepts list or not
    """
    return tag_name in conf["list"]


def get_tag_list(tag_name, tag_value, delimiter):
    """
    Determine tag values
    If tag cannot contain list, we return original value
    If tag can contain a list, we split original value into multiple elements thanks to delimiter
    """
    result = []
    if is_tag_list(tag_name, conf_tag):
        if delimiter in tag_value:
            result.append(tag_value)
            values = tag_value.rsplit(delimiter, 1)
            while len(values) > 1:
                result.append(values[0])
                values = values[0].rsplit(delimiter, 1)
        else:
            result.append(tag_value)
    else:
        result.append(tag_value)

    return result


def load_exif_data(file):
    """ Load EXIF data from source file """
    metadata = ImageMetadata(file)
    metadata.read()
    return metadata


def get_exif_data(exif_data, exif_param):
    """
    Return exif parameter from exif data, return None if param not found

    @param:
    - exif_data : all Exif data from file
    - exif_param : EXIF info to retrieve
    """
    try:
        return exif_data[exif_param].raw_value
    except KeyError:
        return None

    return None


def add_or_update_exif_data(exif_data, exif_param, exif_value):
    """
    Add or replace an exif tag
    If tag is identified as a list tag, then an array is added, otherwise single value

    @param:
    - exif_data : all Exif data from file
    - exif_param : EXIF info to retrieve
    - exif_value : Value of the EXIF tag
    """
    if is_tag_list(exif_param, conf_tag):
        exif_data[exif_param] = exif_value
    else:
        exif_data[exif_param] = exif_value[0]

    exif_data.write(preserve_timestamps=True)


def remove_exif_data(exif_data, exif_param):
    """
    Remove a exif Tage

    @param:
    - exif_data : all Exif data from file
    - exif_param : EXIF info to retrieve
    """
    exif_data._delete_xmp_tag(exif_param)
    exif_data.write(preserve_timestamps=True)


def is_exif_data_exists(exif_data, exif_param):
    """
    Return true if an exif tag exists, false otherwise
    """
    return get_exif_data(exif_data, exif_param) is None
