import pytest

from number_parser import parse, parse_number, NUMERAL_SYSTEMS

all_numeral_systems_but_roman = [system for system in NUMERAL_SYSTEMS if system != 'roman']
all_numeral_systems_but_decimal = [system for system in NUMERAL_SYSTEMS if system != 'decimal']


@pytest.mark.parametrize(
    "test_string, numeral_systems, expected",
    [
        ('Built in MMLXXVII.', None, 'Built in 2077.'),
        ('Built in MMLXXVII.', ['roman'], 'Built in 2077.'),
        ('I was given two IV injections.', all_numeral_systems_but_roman, 'I was given 2 IV injections.'),
        ('I was given two IV injections.', all_numeral_systems_but_decimal, '1 was given two 4 injections.'),
        ('I have three apples.', None, '1 have 3 apples.')
    ]
)
def test_supported_numerals(test_string, numeral_systems, expected):
    assert parse(test_string, numeral_systems=numeral_systems) == expected


def test_parse_unsupported_numerals():
    with pytest.raises(ValueError):
        parse('I have six apples.', numeral_systems=['suzhou'])


def test_parse_number_unsupported_numerals():
    with pytest.raises(ValueError):
        parse_number('Two thousand', numeral_systems=['suzhou'])
