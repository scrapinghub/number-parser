import pytest

from number_parser import parse, parse_number


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("I", 1),
        ("IV", 4),
        ("IX", 9),
        ("XIV", 14),
        ("XL", 40),
        ("CDXLIV", 444),
        (" MDCCLXXVI ", 1776),
        ("MMMCMXCIX", 3999),
        ("IIII", None),
        ("IC", None),
        ("VX", None),
        ("MMMM", None),
        ("xiv", None),
        ("Ⅻ", 12),
        ("ⅳ", 4),
        ("ↀ", 1000),
        ("ⅯⅯⅩⅩⅣ", 2024),
        ("Ↄ", None),
    ],
)
def test_parse_number(test_input, expected):
    assert parse_number(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Built in MDCCLXXVI.", "Built in 1776."),
        ("Louis XIV and Louis XV", "Louis 14 and Louis 15"),
        ("I have II hats and three coats", "I have 2 hats and 3 coats"),
        ("Chapter IIII", "Chapter IIII"),
        ("Mix it", "Mix it"),
        ("Chapter Ⅰ, section ⅳ", "Chapter 1, section 4"),
    ],
)
def test_parse(test_input, expected):
    assert parse(test_input, types={"cardinal", "roman"}) == expected


def test_parse_default():
    assert parse("Louis XIV and two dogs") == "Louis XIV and 2 dogs"
