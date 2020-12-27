from photo_workflow.helpers import list_files

def test_list_files_no_recursive_no_pattern():
    res = list_files("./test/resources/sample_files")

    assert len(res) == 2
    assert "./test/resources/sample_files/a_file_1.txt" in res
    assert "./test/resources/sample_files/a_file_2.txt" in res


def test_list_files_no_recursive_pattern():
    res = list_files("./test/resources/sample_files", False, ".*1.*")

    assert len(res) == 1
    assert "./test/resources/sample_files/a_file_1.txt" in res


def test_list_files_recursive_no_pattern():
    res = list_files("./test/resources/sample_files", True)

    assert len(res) == 6
    assert "./test/resources/sample_files/a_file_1.txt" in res
    assert "./test/resources/sample_files/a_file_2.txt" in res
    assert "./test/resources/sample_files/folder_2/a_file_3.txt" in res
    assert "./test/resources/sample_files/folder_1/subfolder_2/a_file_4.txt" in res
    assert "./test/resources/sample_files/folder_1/subfolder_1/a_file_5.txt" in res
    assert "./test/resources/sample_files/folder_1/subfolder_1/a_file_6.txt" in res


def test_list_files_recursive_pattern():
    res = list_files("./test/resources/sample_files", True, ".*4.*")

    assert len(res) == 1
    assert "./test/resources/sample_files/folder_1/subfolder_2/a_file_4.txt" in res

