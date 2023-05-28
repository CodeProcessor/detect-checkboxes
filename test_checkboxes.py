from checkboxes import get_checkboxes_from_pdf

results = {
    "doc1.pdf": {
        "page_1": [True, False, False, True],
        "page_2": [False]
    }
}


def test_checkboxes():
    for _filename, _test_value in results.items():
        _file_path = f"input/{_filename}"
        converted_output = {}
        output = get_checkboxes_from_pdf(_file_path, output=False)
        for _key, _value in output.items():
            converted_output[_key] = [v["contains_pixels"] for v in _value]

        assert _test_value == converted_output
        print(f"File {_file_path} checkboxes are OK!")


if __name__ == '__main__':
    test_checkboxes()
