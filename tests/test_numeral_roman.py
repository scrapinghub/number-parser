import pytest
import csv
import os

from number_parser import parse, parse_number, NUMERAL_SYSTEMS
from tests import PERMUTATION_DIRECTORY

all_numeral_systems_but_roman = [system for system in NUMERAL_SYSTEMS if system != 'roman']
all_numeral_systems_but_decimal = [system for system in NUMERAL_SYSTEMS if system != 'decimal']


@pytest.mark.parametrize(
    "test_string, numeral_systems, expected",
    [
        ('Built in MMLXXVII.', None, 'Built in 2077.'),
        ('Built in MMLXXVII.', ['decimal'], 'Built in MMLXXVII.'),
        ('I was given two IV injections.', all_numeral_systems_but_roman, 'I was given 2 IV injections.'),
        ('I was given two IV injections.', all_numeral_systems_but_decimal, '1 was given two 4 injections.'),
        ('I was given two IV injections.', None, '1 was given 2 4 injections.'),
        ('I have three apples.', all_numeral_systems_but_roman, 'I have 3 apples.')
    ]
)
def test_parse_roman(test_string, numeral_systems, expected):
    assert parse(test_string, numeral_systems=numeral_systems) == expected


def test_parse_all_roman_numbers():
    with open(os.path.join(PERMUTATION_DIRECTORY, 'all_roman_numbers.csv'), "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                assert parse_number(row['text']) == int(row['number'])
            except AssertionError as e:
                raise AssertionError(F"Failed execution of {row['number']},{row['text']}")
