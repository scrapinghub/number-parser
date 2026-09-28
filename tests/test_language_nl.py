import pytest

from number_parser import parse, parse_number

LANG = "nl"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("nul", 0),
        ("één", 1),
        ("zeventien", 17),
        ("eenentwintig", 21),
        ("drieëntwintig", 23),
        ("tachtig", 80),
        ("honderd", 100),
        ("honderdeenentwintig", 121),
        ("negenhonderddertien", 913),
        ("negentienhonderd", 1900),
        ("tweeduizend vierentwintig", 2024),
        ("drie miljoen tweehonderdduizend", 3_200_000),
        ("twee miljard", 2_000_000_000),
    ],
)
def test_parse_number(expected, test_input):
    assert parse_number(test_input, LANG) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "Ik heb drieëntwintig appels en twee peren",
            "Ik heb 23 appels en 2 peren",
        ),
        ("tweede", "tweede"),
    ],
)
def test_parse(expected, test_input):
    assert parse(test_input, LANG) == expected
