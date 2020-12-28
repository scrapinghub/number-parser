import pytest
from number_parser import parse, parse_number
from number_parser.parser import _valid_tokens_by_language, parse_ordinal


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
def test_valid_tokens_by_language(expected, test_input):
    assert _valid_tokens_by_language(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('one hundred twenty three million four hundred fifty six thousand seven hundred \
            and eighty nine', 123_456_789),
        ("चौदह लाख बत्तीस हज़ार पाँच सौ चौबीस", 1_432_524),
        ("тысяче", 1_000),
        ("Dos mil ciento cuarenta y siete millones cuatrocientos ochenta \
            y tres mil seiscientos cuarenta y siete", 2_147_483_647),
    ]
)
def test_parse_number_lang_auto(expected, test_input):
    assert parse_number(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes.",
         "25 cows, 12 chickens and 125 kg of potatoes."),
        ("dos y dos son cuatro cuatro y dos son seis seis y dos son ocho y ocho dieciséis",
         "2 y 2 son 4 4 y 2 son 6 6 y 2 son 8 y 8 16"),
    ]
)
def test_parse_basic_sentences_lang_auto(expected, test_input):
    assert parse(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # 'en'
        ('eleventh', 11),
        ('one hundred and forty second', 142),
        ("two million three thousand and nineteenth", 2_003_019),
    ]
)
def test_parse_ordinal_lang_auto(expected, test_input):
    assert parse_ordinal(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # en
        ('eleventh day of summer', "11 day of summer"),
        ("nineteenth may two thousand", "19 may 2000"),
    ]
)
def test_parse_sentences_ordinal(expected, test_input):
    assert parse(test_input) == expected
