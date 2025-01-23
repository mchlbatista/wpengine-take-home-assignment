import unittest

from conftest import TEST_DATA_PATH, EXPECTED_FILE_NAMES
from file_path_resolver import FilePathResolver


class TestFilePathResolver(unittest.TestCase):
    """
    Test FilePathResolver class
    """

    def test_can_detect_all(self) -> None:
        """
        Resolve the right files from the test data folder.
        """
        # Given
        # When
        fr = FilePathResolver(TEST_DATA_PATH)
        test_files = [str(file_path) for file_path in fr.files]
        # Then
        self.assertEqual(len(EXPECTED_FILE_NAMES), len(test_files))
        for ef in EXPECTED_FILE_NAMES:
            self.assertIn(ef, test_files)
