import unittest
import asyncio

from ddt import ddt, data, unpack
from unittest.mock import AsyncMock, patch, MagicMock

from conftest import EXPECTED_FILE_NAMES, EXPECTED_FILE_ANALYSIS
from xml_reader import XmlReader


@ddt
class TestXmlReader(unittest.TestCase):
    """
    Tests class XmlReader
    """

    def test_can_read(self):
        """
        Async process file
        """
        # Give
        # When
        file_analysis = asyncio.run(XmlReader.read(EXPECTED_FILE_NAMES[0]))
        # Then
        assert file_analysis == EXPECTED_FILE_ANALYSIS

    @patch("xml_reader.XmlReader.read", new_callable=AsyncMock)
    def test_can_read_multiple(self, mock_file_read):
        """
        Async, process files
        """
        # Given
        mock_file_read.return_value = EXPECTED_FILE_ANALYSIS
        # When
        # Then
        self.assertEqual(
            asyncio.run(XmlReader.read_multiple(["test_path"])),
            [EXPECTED_FILE_ANALYSIS],
        )

    @patch("xml_reader.logger.warning")
    def test_can_ignore_file_parsing_error(self, mock_logger_warning):
        """
        Ignore file if a parsing error occurs
        """
        # Give
        mock_logger_warning.return_value = None
        # When
        file_analysis = asyncio.run(XmlReader.read(EXPECTED_FILE_NAMES[-1]))
        # Then
        self.assertEqual(file_analysis, {})
        mock_logger_warning.assert_called_once_with(
            f"A parsing error has occurred when processing file {EXPECTED_FILE_NAMES[-1]}. File will be ignored."
        )

    @patch("xml_reader.logger.warning")
    @patch("xml_reader.aiofiles.open")
    @data(
        (
            FileNotFoundError,
            "And error occurred. File '' does not exist. File will be ignored.",
        ),
        (
            PermissionError,
            "And error occurred. Permission denied for file ''. File will be ignored.",
        ),
        (
            Exception,
            "An unexpected error occurred: . File will be ignored.",
        ),
    )
    @unpack
    def test_cant_access_file(
        self, exception, expected_mgs, mock_read, mock_logger_warning
    ):
        """
        Can't access file
        """
        # Give
        mock_file_context = MagicMock()
        mock_file_context.return_value.__aenter__.side_effect = exception()
        mock_read.side_effect = mock_file_context
        mock_logger_warning.return_value = None
        # When
        file_analysis = asyncio.run(XmlReader.read(""))
        # Then
        self.assertEqual(file_analysis, {})
        mock_logger_warning.assert_called_once_with(expected_mgs)
