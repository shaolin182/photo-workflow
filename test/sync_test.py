from photo_workflow.sync import build_filename_list


def test_build_filename_list_without_suffix():
    input_filename = "2020-12-26_13-43-26.JPG"

    res = build_filename_list(input_filename)

    assert len(res) == 1
    assert "2020-12-26_13-43-26.JPG" in res


def test_build_filename_list_without_suffix_with_index():
    input_filename = "2020-12-26_13-43-26_1.JPG"

    res = build_filename_list(input_filename)

    assert len(res) == 1
    assert "2020-12-26_13-43-26_1.JPG" in res


def test_build_filename_list_with_suffix():
    input_filename = "2020-12-26_13-43-26_D750.JPG"

    res = build_filename_list(input_filename)

    assert len(res) == 2
    assert "2020-12-26_13-43-26_D750.JPG" in res
    assert "2020-12-26_13-43-26.JPG" in res


def test_build_filename_list_with_multiple_suffix():
    input_filename = "2020-12-26_13-43-26_D750_darktable_01.JPG"

    res = build_filename_list(input_filename)

    assert len(res) == 4
    assert "2020-12-26_13-43-26_D750_darktable_01.JPG" in res
    assert "2020-12-26_13-43-26_D750_darktable.JPG" in res
    assert "2020-12-26_13-43-26_D750.JPG" in res
    assert "2020-12-26_13-43-26.JPG" in res


def test_build_filename_list_with_multiple_suffix_and_index():
    input_filename = "2020-12-26_13-43-26_1_D750_darktable_01.JPG"

    res = build_filename_list(input_filename)

    assert len(res) == 4
    assert "2020-12-26_13-43-26_1_D750_darktable_01.JPG" in res
    assert "2020-12-26_13-43-26_1_D750_darktable.JPG" in res
    assert "2020-12-26_13-43-26_1_D750.JPG" in res
    assert "2020-12-26_13-43-26_1.JPG" in res
