#WPEngine Take Home Assignment 2024-2025

## JUnit XML Tests Failure Rate Report Generator

- [JUnit XML Tests Failure Rate Report Generator](#junit-xml-tests-failure-rate-report-generator)
- [Quick Start](#quick-start)
- [Testing](#testing)
- [Details for the curious](#details-for-the-curious)
  - [App Environment](#app-environment)
  - [Considerations](#considerations)


## Quick Start

Build the app image by using the command `make build-image` in the root of the project. Then, run the app by using the following command:
```
./find_flakes <input_dir> <output_file>
```
`find_flakes` is a bash script that will run the container with the given parameters.

*NOTE*: To run `find_flakes` bash script as a system command use the command in the root of the project `make setup`. This will run `export PATH=${PATH}:${PWD}`.

## Testing

To run tests type `make test`. This will build the tests image, run all the tests and  remove the container from the system after it's done. Lint validation is included using `black==24.10.0`. 

```
All done! ✨ 🍰 ✨
12 files would be left unchanged.
============================= test session starts ==============================
platform linux -- Python 3.11.11, pytest-8.3.4, pluggy-1.5.0 -- /usr/local/bin/python3.11
cachedir: .pytest_cache
rootdir: /app
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.24.0
asyncio: mode=Mode.AUTO, default_loop_scope="session"
collecting ... collected 12 items

tests/test_file_path_resolver.py::TestFilePathResolver::test_can_detect_all PASSED [  8%]
tests/test_happy_path.py::TestHappyPath::test_happy_path PASSED          [ 16%]
tests/test_report_generator.py::TestReportGenerator::test_can_create_file PASSED [ 25%]
tests/test_tests_suite_statistics.py::TestTestsSuiteStatistics::test_can_collect_data PASSED [ 33%]
tests/test_tests_suite_statistics.py::TestTestsSuiteStatistics::test_can_collect_test_result PASSED [ 41%]
tests/test_tests_suite_statistics.py::TestTestsSuiteStatistics::test_can_failure_rate_statistics PASSED [ 50%]
tests/test_xml_reader.py::TestXmlReader::test_can_ignore_file_parsing_error PASSED [ 58%]
tests/test_xml_reader.py::TestXmlReader::test_can_read PASSED            [ 66%]
tests/test_xml_reader.py::TestXmlReader::test_can_read_multiple PASSED   [ 75%]
tests/test_xml_reader.py::TestXmlReader::test_cant_access_file_1 PASSED  [ 83%]
tests/test_xml_reader.py::TestXmlReader::test_cant_access_file_2 PASSED  [ 91%]
tests/test_xml_reader.py::TestXmlReader::test_cant_access_file_3 PASSED  [100%]

============================== 12 passed in 0.08s ==============================
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
src/file_path_resolver.py                 12      0   100%
src/logger.py                             12      0   100%
src/main.py                               13      1    92%   31
src/report_generator.py                   12      0   100%
src/tests_suite_statistics.py             30      0   100%
src/xml_reader.py                         36      0   100%
tests/conftest.py                          4      0   100%
tests/test_file_path_resolver.py          10      0   100%
tests/test_happy_path.py                  10      0   100%
tests/test_report_generator.py            14      0   100%
tests/test_tests_suite_statistics.py      27      0   100%
tests/test_xml_reader.py                  33      0   100%
--------------------------------------------------------------------
TOTAL                                    213      1    99%
```

## Details for the curious

### App Environment

- Docker
- Python 3.11
- Bash

### Considerations

https://github.com/testmoapp/junitxml. It will analyze all the files in a given directory "recursively", and only parse the ones with a valid `.xml` extension (`.xml, .XML, .Xml, ...`). Also, files will be ignored when:

- Invalid formatted XML is detected
- File can't be found
- File's permission error occurred
- Any other exception when opening files occurred

A warning will be shown when any of this occurs and details will be provided.

The given directory and output file location needs to be accessible by Docker. They will be mounted in the container at running time. In MacOS Docker Desktop `Settings -> Resources -> File sharing` you can add the directories you need to work with. The running script, `find_flakes` is removing the container from your system after run. This can be modified if it does not match the expected behavior of your automation pipeline by removing the last line of the script: `docker rm find_flakes > /dev/null`.

A detailed lists of dependencies are included in `./src/requirements.txt` and `./tests/requirements.txt`.

To be able to run `find_flakes` as a system command, as instructed in the assignment, the script location need to be added to your system path.

```
export PATH=$PATH:/path/to/script/dir/location
``` 

Then, you can do `find_flakes <input_dir> <output_file>`
