import pytest
from number_parser import parse, parse_number, parse_ordinal
from tests import HUNDREDS_DIRECTORY, PERMUTATION_DIRECTORY
from tests import _test_files
LANG = 'en'


class TestNumberParser():
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ('eleven', 11),
            ("nineteen", 19),
            ('hundred', 100),
            ('one hundred and forty two', 142),
            ('thousand', 1_000),
            ("two thousand and nineteen", 2_019),
            ('million', 1_000_000),
            ("two million three thousand and nineteen", 2_003_019),
            ('two million twenty three thousand and forty nine', 2_023_049),
            ("two million three thousand nine hundred and eighty four", 2_003_984),
            ('billion', 1_000_000_000),
            ('three billion', 3_000_000_000),
            ('three million', 3_000_000),
            ('one hundred twenty three million four hundred fifty six thousand seven hundred \
                and eighty nine', 123_456_789),
            ('nineteen billion and nineteen', 19_000_000_019),
        ]
    )
    def test_parse_number(self, expected, test_input):
        assert parse_number(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("100000", 100_000),
            ("1 2", None),
            ("twenty 1", None),
            ("12341252352314", 12_341_252_352_314),
        ]
    )
    def test_parse_number_digits(self, expected, test_input):
        assert parse_number(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes.",
             "25 cows, 12 chickens and 125 kg of potatoes."),
            ("I have eight cows", "I have 8 cows"),
            ("I have eight cows three bulls and seven hundred and twelve million dollars ",
                "I have 8 cows 3 bulls and 712000000 dollars"),
            ("They just won seventy-five thousand dollars", "They just won 75000 dollars"),
            ("I have eight cows. I don't have eighteen cows", "I have 8 cows. I don't have 18 cows"),
            ("thirty-four cows = thirty four cows", "34 cows = 34 cows"),
            ("thirty       four       cows = thirty four cows", "34 cows = 34 cows"),
            ("the     sun      is     hundred     and   twelve       km     away.",
                "the     sun      is     112 km     away."),
        ]
    )
    def test_parse_basic_sentences(self, expected, test_input):
        assert parse(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("one two three four twenty five.", "1 2 3 4 25."),
            ("one two three four twenty, five.", "1 2 3 4 20, 5."),
            ("three twenty seven.", "3 27."),
        ]
    )
    def test_parse_ambiguity_in_separators(self, expected, test_input):
        assert parse(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("two thousand thousand", "2000 1000"),
            ("two thousand million", "2000000000"),
            ("two thousand two million", "2002000000"),
            ("two thousand, two million", "2000, 2000000"),
            ("two hundred thousand", "200000"),
            ("two thousand hundred", "2100"),
            ("two hundred hundred", "200 100"),
            ("billion twenty three million", "1023000000"),
            ("million million", "1000000 1000000"),
            ("one hundred thousand thousand", "100000 1000")
        ]
    )
    def test_parse_ambiguity_in_multipliers(self, expected, test_input):
        assert parse(test_input, LANG) == expected

    def test_parse_number_till_hundred(self):
        _test_files(HUNDREDS_DIRECTORY, LANG)

    def test_parse_number_permutations(self):
        _test_files(PERMUTATION_DIRECTORY, LANG)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ('eleventh', 11),
            ("nineteenth", 19),
            ('hundredth', 100),
            ('one hundred and forty second', 142),
            ('thousandth', 1_000),
            ("two thousand and fifth", 2_005),
            ('millionth', 1_000_000),
            ("two million three thousand and nineteenth", 2_003_019),
            ('two million twenty three thousand and forty ninth', 2_023_049),
            ("two million three thousand nine hundred and eighty fourth", 2_003_984),
            ('billionth', 1_000_000_000)
        ]
    )
    def test_parse_ordinal(self, expected, test_input):
        assert parse_ordinal(test_input, LANG) == expected
