import pytest
import csv
from number_parser import parse, parse_number
@pytest.mark.parametrize(
    "test_string, numeral_systems, expected",
    [
        ('Built in MMLXXVII', None, 'Built in 2077')
    ]
)
def test_parse_roman(test_string, numeral_systems, expected):
    assert parse(test_string, numeral_systems=numeral_systems) == expected

def test_parse_all_roman_numbers():
    with open('data/permutations/all_roman_numbers.csv', "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                assert parse_number(row['text']) == int(row['number'])
            except AssertionError as e:
                raise AssertionError(F"Failed execution of {row['number']},{row['text']}")
