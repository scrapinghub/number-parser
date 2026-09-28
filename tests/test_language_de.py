import pytest

from number_parser import parse, parse_number

LANG = "de"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("null", 0),
        ("eins", 1),
        ("elf", 11),
        ("achtzehn", 18),
        ("einundzwanzig", 21),
        ("Dreißig", 30),
        ("dreissig", 30),
        ("neunundneunzig", 99),
        ("hundert", 100),
        ("hundertundeins", 101),
        ("Einhunderteinundzwanzig", 121),
        ("neunhundertdreizehn", 913),
        ("zweitausendeins", 2001),
        ("fünftausendneunhundertdreizehn", 5913),
        ("fünfundzwanzigtausend", 25000),
        ("achtzehnhundertfünfzig", 1850),
        (
            "zwei Millionen dreihundertfünfundvierzigtausendsechshundertachtundsiebzig",
            2_345_678,
        ),
        ("eine Milliarde", 1_000_000_000),
        ("tausend Millionen", 1_000_000_000),
        ("drei Billionen", 3_000_000_000_000),
        ("dreiund", None),
        ("unddrei", None),
    ],
)
def test_parse_number(expected, test_input):
    assert parse_number(test_input, LANG) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "Ich habe dreiundzwanzig Äpfel und zwei Birnen",
            "Ich habe 23 Äpfel und 2 Birnen",
        ),
        ("Achtung, elf Elfen!", "Achtung, 11 Elfen!"),
        ("drei und vier", "3 und 4"),
    ],
)
def test_parse(expected, test_input):
    assert parse(test_input, LANG) == expected
