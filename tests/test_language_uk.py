import pytest
from number_parser import parse_number
from tests import HUNDREDS_DIRECTORY, PERMUTATION_DIRECTORY
from tests import _test_files

LANG = 'uk'


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("нуль", 0),
        ("нулю", 0),
        ("мільйон", 1_000_000),
        ("міліон", 1_000_000),
    ]
)
def test_parse_number(expected, test_input):
    assert parse_number(test_input, LANG) == expected


def test_parse_number_till_hundred():
    _test_files(HUNDREDS_DIRECTORY, LANG)


def test_parse_number_permutations():
    _test_files(PERMUTATION_DIRECTORY, LANG)
