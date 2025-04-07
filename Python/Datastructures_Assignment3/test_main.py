import pytest
import main
import os


@pytest.mark.parametrize("word, file_path", [("höna", "TestData/tak.txt"),
                                             ("Vatten", "TestData/Drycker/Cola.txt"),
                                             ("Horn", "TestData/Gnu.tx")])
def test_error_is_in_file(word, file_path):
    """ Test if error is raised when file does not exist. """
    with pytest.raises(FileNotFoundError):
        main.is_in_file(word, file_path)


@pytest.mark.parametrize("word, file_path, expected_output",
                         [("vatten", "TestData/Makaroner.txt", True),
                          ("VATTEN", "TestData/Gnu.txt", False),
                          ("VATTEN", "TestData/Drycker/Vatten.txt", True),
                          ("AspArtaM", "TestData/Drycker/KoffeinDrycker/ColaZero.txt", True)])
def test_is_in_file(word, file_path, expected_output):
    """ Test if word is in file. """
    assert main.is_in_file(word, file_path) == expected_output


@pytest.mark.parametrize("search_word, search_dir, expected_output",
                         [("Vatten", "TestData",
                           f"""{os.path.abspath("TestData/Drycker/KoffeinDrycker/ColaZero.txt")}
{os.path.abspath("TestData/Drycker/KoffeinDrycker/Kaffe.txt")}
{os.path.abspath("TestData/Drycker/Vatten.txt")}
{os.path.abspath("TestData/Makaroner.txt")}\n"""),
                          ("Koffein", "TestData",
                           f"""{os.path.abspath("TestData/Drycker/KoffeinDrycker/ColaZero.txt")}
{os.path.abspath("TestData/Drycker/KoffeinDrycker/Kaffe.txt")}\n""")])
def test_get_paths_for_word(search_word, search_dir, expected_output):
    """ Test if the path returned is the same as the expected paths. """
    assert main.get_paths_for_word(search_word, search_dir) == expected_output
