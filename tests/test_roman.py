import csv
import os

from number_parser import parse_number, NUMERAL_SYSTEMS
from tests import PERMUTATION_DIRECTORY

all_numeral_systems_but_roman = [system for system in NUMERAL_SYSTEMS if system != 'roman']
all_numeral_systems_but_decimal = [system for system in NUMERAL_SYSTEMS if system != 'decimal']


def test_parse_all_roman_numbers():
    with open(os.path.join(PERMUTATION_DIRECTORY, 'all_roman_numbers.csv'), "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                assert parse_number(row['text']) == int(row['number'])
            except AssertionError as e:
                raise AssertionError(F"Failed execution of {row['number']},{row['text']}")


def test_incorrect_roman_numbers():
    with open(os.path.join(PERMUTATION_DIRECTORY, 'incorrect_roman_numbers.csv'), "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                assert parse_number(row['text']) == int(row['number'])
            except AssertionError as e:
                raise AssertionError(F"Failed execution of {row['number']},{row['text']}")
