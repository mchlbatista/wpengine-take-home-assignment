# Happy Path Test
#
# Test when given the right parameters,
# the whole app can run and deliver the expected results.

import csv
import unittest

from main import process_junit_files, OUTPUT_FILE_PATH


class TestHappyPath(unittest.TestCase):
    """
    Happy Path Test
    """

    def test_happy_path(self):
        """
        When given the right parameters,
        the whole app can run and deliver the expected results.
        """
        process_junit_files()
        with open(OUTPUT_FILE_PATH, mode="r") as file_report:
            reader = csv.DictReader(file_report)
            file_content = list(reader)
            self.assertEqual(
                file_content,
                [
                    {"test_name": "test 2", "failure_rate": "50.0%"},
                    {"test_name": "test 3", "failure_rate": "80.0%"},
                    {"test_name": "test 6", "failure_rate": "50.0%"},
                    {"test_name": "test 9", "failure_rate": "75.0%"},
                    {"test_name": "test 17", "failure_rate": "50.0%"},
                    {"test_name": "test 22", "failure_rate": "100.0%"},
                ],
            )
