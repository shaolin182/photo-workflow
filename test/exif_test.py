from photo_workflow.helpers import conf_tag
from photo_workflow import exif
# from photo_workflow.exif import load_exif_data, get_exif_data, remove_exif_data, add_or_update_exif_data, is_tag_list, get_tag_list, tag_process

def test_load_exif_tag():

    # Load all exif data
    exif_data = exif.load_exif_data("./test/resources/2013-06-01_10-08-04_Julien.NEF")

    # Load specific XMP tag
    exif_hierarchical_subject = exif.get_exif_data(exif_data, "Xmp.lr.hierarchicalSubject")
    exif_subject = exif.get_exif_data(exif_data, "Xmp.dc.Subject")

    # Assertions
    assert isinstance(exif_hierarchical_subject, list)
    assert "Sorties" in exif_hierarchical_subject
    assert "Sorties|2013" in exif_hierarchical_subject
    assert "Sorties|2013|Evenement" in exif_hierarchical_subject
    assert "Sorties|2013|Evenement|Roland_Garros" in exif_hierarchical_subject
    assert exif_subject == "Sorties|2013|Evenement|Roland_Garros"


def test_add_exif_tag():

    # Load all exif data
    exif_data = exif.load_exif_data("./test/resources/2013-06-01_10-08-04_Julien.NEF")

    # Load specific XMP tag
    exif.add_or_update_exif_data(exif_data, "Xmp.lr.PrivateRTKInfo", ["test_value"])
    result = exif.get_exif_data(exif_data, "Xmp.lr.PrivateRTKInfo")

    # Assertions
    assert result.decode("utf-8") == "test_value"


def test_update_exif_tag():

    # Load all exif data
    exif_data = exif.load_exif_data("./test/resources/2013-06-01_10-08-04_Julien.NEF")

    # Load specific XMP tag
    exif.add_or_update_exif_data(exif_data, "Xmp.lr.PrivateRTKInfo", ["test_value_update"])
    result = exif.get_exif_data(exif_data, "Xmp.lr.PrivateRTKInfo")

    # Assertions
    assert result.decode("utf-8") == "test_value_update"


def test_remove_exif_tag():

    # Load all exif data
    exif_data = exif.load_exif_data("./test/resources/2013-06-01_10-08-04_Julien.NEF")

    # Load specific XMP tag
    exif.remove_exif_data(exif_data, "Xmp.lr.PrivateRTKInfo")
    exif_hierarchical_subject = exif.get_exif_data(exif_data, "Xmp.lr.PrivateRTKInfo")

    # Assertions
    assert exif_hierarchical_subject is None


def test_tag_conf():
    assert exif.is_tag_list('Xmp.dc.Subject', conf_tag) is False
    assert exif.is_tag_list('Xmp.lr.hierarchicalSubject', conf_tag) is True


def test_get_tag_list():
    result = exif.get_tag_list("Xmp.lr.hierarchicalSubject", "Sorties|2018|France|Rennes", "|")

    assert len(result) == 4
    assert "Sorties|2018|France|Rennes" in result
    assert "Sorties|2018|France" in result
    assert "Sorties|2018" in result
    assert "Sorties" in result

    result = exif.get_tag_list("Xmp.lr.hierarchicalSubject", "Sorties", "|")
    assert len(result) == 1
    assert "Sorties" in result

    result = exif.get_tag_list("Xmp.dc.Subject", "Sorties|2018|France|Rennes", "|")

    assert len(result) == 1
    assert "Sorties|2018|France|Rennes" in result


def test_tag_process_add(mocker):

    mock_list_files = mocker.patch.object(exif, 'list_files', return_value=["some_file.txt", "some_other_file.txt"])
    mock_load = mocker.patch.object(exif, 'load_exif_data')
    mock_add_tag = mocker.patch.object(exif, 'add_or_update_exif_data')

    exif.tag_process("./path/to/source", "Xmp.lr.hierarchicalSubject", "Sorties|2018|France|Rennes", "|", False,False)

    mock_list_files.assert_called_once_with("./path/to/source", False, None, False)
    assert mock_load.call_count == 2
    assert mock_add_tag.call_count == 2


def test_tag_process_remove(mocker):

    mock_list_files = mocker.patch.object(exif, 'list_files', return_value=["some_file.txt", "some_other_file.txt"])
    mock_load = mocker.patch.object(exif, 'load_exif_data')
    mock_rm_tag = mocker.patch.object(exif, 'remove_exif_data')

    exif.tag_process("./path/to/source", "Xmp.lr.hierarchicalSubject", "Sorties|2018|France|Rennes", "|", True,False)

    mock_list_files.assert_called_once_with("./path/to/source", False, None, False)
    assert mock_load.call_count == 2
    assert mock_rm_tag.call_count == 2

    




