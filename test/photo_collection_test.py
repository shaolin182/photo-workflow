from photo_collection.photo_collection import PhotoCollection

def test_get_related_collections():

    collection = PhotoCollection()
    res = list_files("./test/resources/sample_files")

    assert len(res) == 2
    assert "./test/resources/sample_files/a_file_1.txt" in res
    assert "./test/resources/sample_files/a_file_2.txt" in res