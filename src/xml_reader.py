import asyncio
import aiofiles
import xml.etree.ElementTree as ET

from logger import logger


class XmlReader(object):
    """
    Collection of tooling for loading JUnit XML files and extract required data.
    """

    @staticmethod
    async def read_multiple(file_paths: list) -> list:
        """
        Read multiple files concurrently
        """
        logger.info(f"Parsing {len(file_paths)} files. Please wait.")
        # This will open/read all the discovered files concurrently.
        # Depending of the expected count of files, we could do this here by batches
        # and not just read all of them at the same time like I'm doing here.
        tasks = [XmlReader.read(file_path) for file_path in file_paths]
        return await asyncio.gather(*tasks)

    @staticmethod
    async def read(file_path: str) -> list:
        """
        Read the given XML file (path) and extract tests and their Success status.

        Expected return format:
        {
            'test 1': True,
            'test 2': False,
            'test 3': False,
            'test 4': True,
            'test 5': True,
            'test 6': True,
            'test 7': True,
            'test 8': True,
            'test 9': False,
            'test 10': True
        }
        """

        content = None
        try:
            async with aiofiles.open(
                file_path, mode="r", encoding="utf-8"
            ) as tests_xml:
                content = await tests_xml.read()
        except FileNotFoundError:
            logger.warning(
                f"And error occurred. File '{file_path}' does not exist. File will be ignored."
            )
        except PermissionError:
            logger.warning(
                f"And error occurred. Permission denied for file '{file_path}'. File will be ignored."
            )
        except Exception as e:
            logger.warning(f"An unexpected error occurred: {e}. File will be ignored.")

        test_summary = {}
        if content:
            try:
                xml_root = ET.fromstring(content)
                # Collect all "testcase" elements present on the JUnit file.
                # This will cover all nested elements.
                for element in xml_root.iter("testcase"):
                    test_name = element.get("name")
                    # We expect a 'name' to be present. If not, we will be unable
                    # to create a cross relationship with other tests in different files.
                    # Then, if 'name' is not present we will skip the tests statistics
                    # process for this specific test.
                    if test_name:
                        test_summary[test_name] = True
                        failure = element.find("failure")
                        if failure is not None:
                            test_summary[test_name] = False
            except ET.ParseError as e:
                logger.warning(
                    f"A parsing error has occurred when processing file {file_path}. File will be ignored."
                )

        return test_summary
