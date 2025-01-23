from file_path_resolver import FilePathResolver
from xml_reader import XmlReader


class TestsSuiteStatistics(object):
    """
    Tooling for loading JUnit XML reports and create statistics.
    """

    @staticmethod
    async def collect_data(data_path: str) -> list:
        """
        Groups all the data from the JUnit XML files

        Expected return format:
        [
            # File 1.xml
            {
                'test 1': {'passed': 2, 'failed': 0},
                'test 2': {'passed': 1, 'failed': 1},
            },
            # File 2.xml
            {
                'test 1': {'passed': 2, 'failed': 0},
                'test 2': {'passed': 1, 'failed': 1},
            },
            ...
        ]
        """
        path_resolver = FilePathResolver(data_path)
        compiled_results = await XmlReader.read_multiple(path_resolver.files)
        return compiled_results

    @staticmethod
    def failure_rate_statistics(compiled_results: list) -> list:
        """
        Process the parsed tests results and generates the failure rate statistics

        Expected return format:
        [
            {'test_name': 'test 1, 'failure_rate': '50.0%'},
            {'test_name': 'test 2, 'failure_rate': '100.0%'},
            ...
        ]
        """
        tests_statistic = TestsSuiteStatistics.collect_test_results(compiled_results)
        results = []
        for t in tests_statistic:
            if tests_statistic[t]["failed"] > 0:
                total_tests = (
                    tests_statistic[t]["passed"] + tests_statistic[t]["failed"]
                )
                failure_rate = (tests_statistic[t]["failed"] / total_tests) * 100
                results.append(
                    {"test_name": t, "failure_rate": f"{round(failure_rate, 2)}%"}
                )
        return results

    @staticmethod
    def collect_test_results(compiled_results: list) -> dict:
        """
        Process the data from the JUnit files and extract Success/Failure statistics.
        This will cover the case where if a test is only present in some files. It will be analyzed as well.

        Expected return format:
        {
            'test 1': {'passed': 2, 'failed': 0},
            'test 2': {'passed': 1, 'failed': 1},
            ...
        }
        """
        test_results = {}
        if compiled_results:
            # Walk every report
            for t in compiled_results:
                # Collect the data for every test
                for k in t:
                    if k not in test_results:
                        test_results[k] = {"passed": 0, "failed": 0}
                    # Collecting the count of success/failure.
                    # The Sum of both will be the total runs of the test.
                    if t[k]:
                        test_results[k]["passed"] += 1
                    else:
                        test_results[k]["failed"] += 1
        return test_results
