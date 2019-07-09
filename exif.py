import piexif

def load_exif_data(file):
    """ Load EXIF data from source file """
    return piexif.load(file)

def get_exif_data(exif_data, exif_param):
    """
    Return exif parameter from exif data, return None if param not found
    
    @param:
    - exif_data : all Exif data from file
    - exif_param : EXIF info to retrieve
    """
    if exif_param in exif_data["Exif"]:
        return exif_data["Exif"][exif_param]

    return None