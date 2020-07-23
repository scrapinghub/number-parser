import os
import csv
import sys
import logging
from number_parser import parse_number

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
HUNDREDS_DIRECTORY = os.path.join(TEST_ROOT, "./data/hundreds")
PERMUTATION_DIRECTORY = os.path.join(TEST_ROOT, "./data/permutations")


def get_test_files(path, prefix):
    return [
        os.path.join(path, filename)
        for filename in os.listdir(path)
        if filename.startswith(prefix)
    ]


def _test_files(path, language):
    for filename in get_test_files(path, f'{language}_'):
        with open(filename, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                try:
                    assert parse_number(row['text'], language) == int(row['number'])
                except AssertionError:
                    logging.error(F"Failed execution of {row['text']}", exc_info=True)
                    sys.exit()
