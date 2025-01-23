import os
import asyncio

from report_generator import ReportGenerator
from tests_suite_statistics import TestsSuiteStatistics


# Designed to run in a container.
# What we do here is stablish where the data will be in the container (DATA_PATH).
# Stablish where the final report will be as well (OUTPUT_FILE = "/app/output_files"),
# but using the given final report name (evar 'OUTPUT_FILE')
DATA_PATH = "/app/data"
ROOT_OUTPUT_FILE_PATH = "/app/output_files"
OUTPUT_FILE_PATH = os.path.join(
    ROOT_OUTPUT_FILE_PATH, os.getenv("OUTPUT_FILE", "output.csv")
)


def process_junit_files():
    # Collect and parse the data async.
    compiled_results = asyncio.run(TestsSuiteStatistics.collect_data(DATA_PATH))
    # Generate Statistics
    failure_rate_statistics = TestsSuiteStatistics.failure_rate_statistics(
        compiled_results
    )
    # Create the final report
    ReportGenerator.failure_rate(failure_rate_statistics, OUTPUT_FILE_PATH)


if __name__ == "__main__":
    process_junit_files()
