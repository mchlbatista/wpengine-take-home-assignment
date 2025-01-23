import unittest
import asyncio

from unittest.mock import AsyncMock, patch, PropertyMock

from conftest import EXPECTED_FILE_ANALYSIS
from tests_suite_statistics import TestsSuiteStatistics


class TestTestsSuiteStatistics(unittest.TestCase):
    """
    Test class TestsSuiteStatistics
    """

    EXPECTED_JUNIT_COMPILED_RESULTS = [EXPECTED_FILE_ANALYSIS, EXPECTED_FILE_ANALYSIS]

    EXPECTED_TEST_STATISTICS = {
        "test 1": {"passed": 2, "failed": 0},
        "test 2": {"passed": 2, "failed": 0},
        "test 3": {"passed": 0, "failed": 2},
        "test 4": {"passed": 2, "failed": 0},
        "test 5": {"passed": 2, "failed": 0},
        "test 6": {"passed": 0, "failed": 2},
        "test 7": {"passed": 2, "failed": 0},
        "test 8": {"passed": 2, "failed": 0},
        "test 9": {"passed": 0, "failed": 2},
        "test 10": {"passed": 2, "failed": 0},
    }

    EXPECTED_FAILURE_RATE = [
        {"test_name": "test 3", "failure_rate": "100.0%"},
        {"test_name": "test 6", "failure_rate": "100.0%"},
        {"test_name": "test 9", "failure_rate": "100.0%"},
    ]

    @patch("tests_suite_statistics.FilePathResolver.__init__", return_value=None)
    @patch("tests_suite_statistics.XmlReader.read_multiple", new_callable=AsyncMock)
    @patch("tests_suite_statistics.FilePathResolver.files", new_callable=PropertyMock)
    def test_can_collect_data(
        self, mock_file_resolver_files, mock_read_multiple, mock_file_resolver
    ):
        """
        Run the logic that collects data from files

        - FilePathResolver called with the expected arguments
        - XmlReader.read_multiple called with the expected arguments
        - XmlReader.read_multiple and the function returns the expected result
        """
        # Given
        expected_file_paths = ["test_file_path"]
        expected_data_path = "test_data_path"
        # When
        mock_read_multiple.return_value = [EXPECTED_FILE_ANALYSIS]
        mock_file_resolver_files.return_value = expected_file_paths
        # Then
        self.assertEqual(
            asyncio.run(TestsSuiteStatistics.collect_data(expected_data_path)),
            [EXPECTED_FILE_ANALYSIS],
        )
        mock_read_multiple.assert_called_once_with(expected_file_paths)
        mock_file_resolver.assert_called_once_with(expected_data_path)

    def test_can_collect_test_result(self):
        """
        Generate the expected test statistics
        """
        # Given
        # When
        compiled_results = TestsSuiteStatistics.collect_test_results(
            self.EXPECTED_JUNIT_COMPILED_RESULTS
        )
        # Then
        self.assertEqual(compiled_results, self.EXPECTED_TEST_STATISTICS)

    @patch(
        "tests_suite_statistics.TestsSuiteStatistics.collect_test_results",
        return_value=EXPECTED_TEST_STATISTICS,
    )
    def test_can_failure_rate_statistics(self, mock_collect_results):
        """
        Generate the expected failure rate collection for the given data
        """
        # Given
        # When
        failure_rate_statistics = TestsSuiteStatistics.failure_rate_statistics(
            self.EXPECTED_JUNIT_COMPILED_RESULTS
        )
        # Then
        self.assertEqual(failure_rate_statistics, self.EXPECTED_FAILURE_RATE)
