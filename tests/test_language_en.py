from number_parser import parser
import pytest

LANG = 'en'


class TestNumberParser():
    @pytest.mark.parametrize(
        "expected,test_input",
        [
            (2003984, "two million three thousand nine hundred and eighty four"),
            (19, "nineteen"),
            (2019, "two thousand and nineteen"),
            (2003019, "two million three thousand and nineteen"),
            (3000000000, 'three billion'),
            (3000000, 'three million'),
            (123456789, 'one hundred twenty three million four hundred fifty six thousand seven hundred \
                and eighty nine'),
            (11, 'eleven'),
            (19000000019, 'nineteen billion and nineteen'),
            (142, 'one hundred and forty two'),
            (2023049, 'two million twenty three thousand and forty nine'),
            (100, 'hundred'),
            (1000, 'thousand'),
            (1000000, 'million'),
            (1000000000, 'billion'),

        ]
    )
    def test_parse_number(self, expected, test_input):
        assert parser.parse_number(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "expected,test_input",
        [
            (100000, "100000"),
            (None, "1 2"),
            (None, "twenty 1"),
            (12341252352314, "12341252352314"),
            (21, 'twenty-one'),
            (365, 'three-hundred and sixty-five'),
        ]
    )
    def test_parse_number_digits(self, expected, test_input):
        assert parser.parse_number(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes.",
                "25 cows, 12 chickens and 125 kg of potatoes."),

            ("I have eight cows",
                "I have 8 cows"),

            ("I have eight cows three bulls and seven hundred and twelve million dollars ",
                "I have 8 cows 3 bulls and 712000000 dollars"),

            ("They just won seventy-five thousand dollars",
                "They just won 75000 dollars"),

            ("I have eight cows. I don't have eighteen cows",
                "I have 8 cows. I don't have 18 cows"),

            ("thirty-four cows = thirty four cows",
                "34 cows = 34 cows"),

            ("thirty       four       cows = thirty four cows",
                "34 cows = 34 cows"),

            ("the     sun      is     hundred     and   twelve       km     away.",
                "the     sun      is     112 km     away."),
        ]
    )
    def test_basic_sentences(self, expected, test_input):
        assert parser.parse(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("one two three four twenty five.",
                "1 2 3 4 25."),

            ("one two three four twenty, five.",
                "1 2 3 4 20, 5."),

            ("three twenty seven.",
                "3 27."),
        ]
    )
    def test_ambiguity_in_separators(self, expected, test_input):
        assert parser.parse(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("OnE DaY at a Time.",
                "1 DaY at a Time."),

            ("SeVentY THREE days of SUMMER!!!.",
                "73 days of SUMMER!!!."),

            ("Twelve 11 pm",
                "12 11 pm"),
        ]
    )
    def test_case_of_string(self, expected, test_input):
        assert parser.parse(test_input, LANG) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("two thousand thousand",
                "2000 1000"),

            ("two thousand million",
                "2000000000"),

            ("two thousand two million",
                "2002000000"),

            ("two thousand, two million",
                "2000, 2000000"),

            ("two hundred thousand",
                "200000"),

            ("two thousand hundred",
                "2100"),

            ("two hundred hundred",
                "200 100"),

            ("million twenty three billion",
                "1000023000000000"),

            ("billion twenty three million",
                "1000000023 1000000"),

            ("million million",
                "1000000 1000000")
        ]
    )
    def test_ambiguity_in_multipliers(self, expected, test_input):
        assert parser.parse(test_input, LANG) == expected
