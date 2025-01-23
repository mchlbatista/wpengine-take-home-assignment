import os
import csv
import unittest

from conftest import TEST_DATA_PATH
from report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    """
    Test ReportGenerator class
    """

    TEST_REPORT_DATA = [
        {"test_name": "test 00", "failure_rate": "100%"},
        {"test_name": "test 01", "failure_rate": "20%"},
        {"test_name": "test 02", "failure_rate": "30%"},
        {"test_name": "test 03", "failure_rate": "10%"},
        {"test_name": "test 04", "failure_rate": "1%"},
    ]

    def test_can_create_file(self):
        """
        Create the report.
        Reports contains the expected data
        (TestReportGenerator.TEST_REPORT_DATA)
        """
        # Given
        # When
        report_file_path = os.path.join(TEST_DATA_PATH, "test_file.csv")
        ReportGenerator.failure_rate(self.TEST_REPORT_DATA, report_file_path)
        # Then
        with open(report_file_path, mode="r") as file_report:
            reader = csv.DictReader(file_report)
            file_content = list(reader)
            self.assertEqual(file_content, self.TEST_REPORT_DATA)
