import pytest
from number_parser import parse, parse_number, parse_ordinal, _valid_tokens_by_language


class TestNumberParser():
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ('eleven', 11),
            ('one hundred and forty two', 142),
            ("two thousand and nineteen", 2_019),
            ("two million three thousand and nineteen", 2_003_019),
            ('billion', 1_000_000_000),
            ('one hundred twenty three million four hundred fifty six thousand seven hundred \
                and eighty nine', 123_456_789),
            ('nineteen billion and nineteen', 19_000_000_019),
            ("छह सौ छियासठ", 666),
            ("एक लाख", 100000),
            ("चौदह लाख बत्तीस हज़ार पाँच सौ चौबीस", 1_432_524),
            ("пятьсот девяносто шесть", 596),
            ("пятьюстами девяноста шестью", 596),
            ("пятистах девяноста шести", 596),
            ("тысяче", 1_000),
            ("Dos mil ciento cuarenta y siete millones cuatrocientos ochenta \
                y tres mil seiscientos cuarenta y siete", 2_147_483_647),
            ("tres mil millones veinticuatro", 3_000_000_024),
            ("tres mil veintitrés millones mil cuatrocientos treinta y dos", 3_023_001_432),
        ]
    )
    def test_parse_number(self, expected, test_input):
        assert parse_number(test_input) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes.",
             "25 cows, 12 chickens and 125 kg of potatoes."),
            ("I have eight cows", "I have 8 cows"),
            ("I have eight cows three bulls and seven hundred and twelve million dollars ",
                "I have 8 cows 3 bulls and 712000000 dollars"),
            ("thirty       four       cows = thirty four cows", "34 cows = 34 cows"),
            ("the     sun      is     hundred     and   twelve       km     away.",
                "the     sun      is     112 km     away."),
            ("dos y dos son cuatro cuatro y dos son seis seis y dos son ocho y ocho dieciséis",
             "2 y 2 son 4 4 y 2 son 6 6 y 2 son 8 y 8 16"),
            ("doscientos cincuenta y doscientos treinta y uno y doce", "250 y 231 y 12"),
        ]
    )
    def test_parse_basic_sentences(self, expected, test_input):
        assert parse(test_input) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes.", "en"),
            ("I have eight cows", "en"),
            ("dos y dos son cuatro cuatro y dos son seis seis y dos son ocho y ocho dieciséis", "es"),
            ("doscientos cincuenta y doscientos treinta y uno y doce", "es"),
            ("robust", "en"),
            ("y y y one y y", "es"),  # y is the skip token for Spanish and dominates.
            ("qwertyuiop", "en"),
            ("тысяче testing", "ru"),
            ("dos two двух", "en"),  # Code-mix data with equal counts , no guarentee.
            ("एक लाख five", "hi")
        ]
    )
    def test_valid_tokens_by_language(self, expected, test_input):
        assert _valid_tokens_by_language(test_input) == expected
