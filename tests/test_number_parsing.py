import pytest
from number_parser import parse, parse_number
from number_parser.parser import LanguageData, parse_ordinal


@pytest.mark.parametrize(
    "test_input,expected,lang",
    [
        # empty / not-a-number
        ('', None, None),
        ('example of sentence', None, None),
        # numeric
        ('32', 32, None),
        (' 3 ', 3, None),
        # en
        ('eleven', 11, 'en'),
        ('one hundred and forty two', 142, 'en'),
        ("two thousand and nineteen", 2_019, 'en'),
        ("two million three thousand and nineteen", 2_003_019, 'en'),
        ('billion', 1_000_000_000, 'en'),
        ('one hundred twenty three million four hundred fifty six thousand seven hundred \
            and eighty nine', 123_456_789, 'en'),
        ('nineteen billion and nineteen', 19_000_000_019, 'en'),
        # hi
        ("छह सौ छियासठ", 666, 'hi'),
        ("एक लाख", 100000, 'hi'),
        ("चौदह लाख बत्तीस हज़ार पाँच सौ चौबीस", 1_432_524, 'hi'),
        # ru
        ("пятьсот девяносто шесть", 596, 'ru'),
        ("пятьюстами девяноста шестью", 596, 'ru'),
        ("пятистах девяноста шести", 596, 'ru'),
        ("тысяче", 1_000, 'ru'),
        # es
        ("Dos mil ciento cuarenta y siete millones cuatrocientos ochenta \
            y tres mil seiscientos cuarenta y siete", 2_147_483_647, 'es'),
        ("tres mil millones veinticuatro", 3_000_000_024, 'es'),
        ("tres mil veintitrés millones mil cuatrocientos treinta y dos", 3_023_001_432, 'es'),
    ]
)
def test_parse_number(expected, test_input, lang):
    assert parse_number(test_input, language=lang) == expected


@pytest.mark.parametrize(
    "test_input,expected,lang",
    [
        # en
        ("twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes.",
         "25 cows, 12 chickens and 125 kg of potatoes.", 'en'),
        ("I have eight cows", "I have 8 cows", 'en'),
        ("I have eight cows three bulls and seven hundred and twelve million dollars ",
            "I have 8 cows 3 bulls and 712000000 dollars", 'en'),
        ("thirty       four       cows = thirty four cows", "34 cows = 34 cows", 'en'),
        ("the     sun      is     hundred     and   twelve       km     away.",
            "the     sun      is     112 km     away.", 'en'),
        # es
        ("dos y dos son cuatro cuatro y dos son seis seis y dos son ocho y ocho dieciséis",
         "2 y 2 son 4 4 y 2 son 6 6 y 2 son 8 y 8 16", 'es'),
        ("doscientos cincuenta y doscientos treinta y uno y doce", "250 y 231 y 12", 'es'),
    ]
)
def test_parse_basic_sentences(expected, test_input, lang):
    assert parse(test_input, lang) == expected


@pytest.mark.parametrize(
    "test_input,expected,lang",
    [
        ("OnE DaY at a Time.", "1 DaY at a Time.", 'en'),
        ("SeVentY THREE days of SUMMER!!!.", "73 days of SUMMER!!!.", 'en'),
        ("Twelve 11 pm", "12 11 pm", 'en'),
    ]
)
def test_parse_case_of_string(expected, test_input, lang):
    assert parse(test_input, lang) == expected


@pytest.mark.parametrize(
    "test_input,expected,lang",
    [
        # 'en'
        ('eleventh', 11, 'en'),
        ("nineteenth", 19, 'en'),
        ('hundredth', 100, 'en'),
        ('one hundred and forty second', 142, 'en'),
        ('thousandth', 1_000, 'en'),
        ("two thousand and fifth", 2_005, 'en'),
        ('millionth', 1_000_000, 'en'),
        ("two million three thousand and nineteenth", 2_003_019, 'en'),
        ('two million twenty three thousand and forty ninth', 2_023_049, 'en'),
        ("two million three thousand nine hundred and eighty fourth", 2_003_984, 'en'),
        ('billionth', 1_000_000_000, 'en'),
        ('with goldsmith', None, 'en'),
        ('th th', None, 'en'),
        ('fifth fiftieth', None, 'en'),
        # Some ambiguos cases
        ('fiftieth fifth', 55, 'en'),
        ('fiftieth five', 55, 'en'),
        ('fifty five', 55, 'en')
    ]
)
def test_parse_ordinal(expected, test_input, lang):
    assert parse_ordinal(test_input, lang) == expected


@pytest.mark.parametrize(
    "test_input,expected,lang",
    [
        ('eleventh day of summer', "11 day of summer", 'en'),
        ("nineteenth may two thousand", "19 may 2000", 'en'),
        ('hundredth and one', "100 and 1", 'en'),
        ('one hundred and forty second', "142", 'en'),
        ('five thousandth and one', "5000 and 1", 'en'),
        ("thirty seven and fifth", "37 and 5", 'en'),
        ('eighth month of year two thousand and twentieth', "8 month of year 2020", 'en'),
        ('He crieth, a path with fifty fifth steps', "He crieth, a path with 55 steps", 'en'),
        ('twentieth seventh fiftieth third', "20 7 50 3", 'en')
    ]
)
def test_parse_sentences_ordinal(expected, test_input, lang):
    assert parse(test_input, lang) == expected


def test_LanguageData_unsupported_language():
    with pytest.raises(ValueError):
        LanguageData('xxxx')
