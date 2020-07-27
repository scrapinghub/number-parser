import pytest
from number_parser import parse, parse_number
from tests import HUNDREDS_DIRECTORY, PERMUTATION_DIRECTORY
from tests import _test_files
LANG = 'hi'


class TestNumberParser():
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("छब्बीस", 26),
            ("इकतीस", 31),
            ("एक सौ एक", 101),
            ("दो सौ छप्पन", 256),
            ("तीन सौ दो", 302),
            ("तीन सौ बयालीस", 342),
            ("चार सौ चौबीस", 424),
            ("छह सौ छियासठ", 666),
            ("एक लाख", 100000),
            ("चौदह लाख बत्तीस हज़ार पाँच सौ चौबीस", 1_432_524),
            ("एक अरब", 1_000_000_000),
            ("दो अरब चौदह करोड़ चौहत्तर लाख तिरासी हज़ार छह सौ सैंतालीस", 2_147_483_647),
        ]
    )
    def test_parse_number(self, expected, test_input):
        assert parse_number(test_input, LANG) == expected

    def test_parse_number_till_hundred(self):
        _test_files(HUNDREDS_DIRECTORY, LANG)

    def test_parse_number_permutations(self):
        _test_files(PERMUTATION_DIRECTORY, LANG)
