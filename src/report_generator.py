import os
import csv

from logger import logger


class ReportGenerator(object):
    """
    Writes the final Tests Report
    """

    REPORT_HEADERS = ["test_name", "failure_rate"]

    @staticmethod
    def failure_rate(statistic: list, output_file: str):
        """
        Writes statistics to the final file
        """
        with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ReportGenerator.REPORT_HEADERS)
            writer.writeheader()
            writer.writerows(statistic)
            logger.info(f"Report written to: {os.path.basename(output_file)}")
