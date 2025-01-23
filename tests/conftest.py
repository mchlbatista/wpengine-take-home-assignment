import os


TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
EXPECTED_FILE_NAMES = [
    f"{TEST_DATA_PATH}/1.Xml",
    f"{TEST_DATA_PATH}/2.XML",
    f"{TEST_DATA_PATH}/3.xml",
    f"{TEST_DATA_PATH}/new_test_folder/1.xml",
    f"{TEST_DATA_PATH}/new_test_folder/4.xml",
    f"{TEST_DATA_PATH}/new_test_folder/5.xml",
    f"{TEST_DATA_PATH}/new_test_folder/6.xml",
]
EXPECTED_FILE_ANALYSIS = {
    "test 1": True,
    "test 2": True,
    "test 3": False,
    "test 4": True,
    "test 5": True,
    "test 6": False,
    "test 7": True,
    "test 8": True,
    "test 9": False,
    "test 10": True,
}
