import pytest

from number_parser import parse_number
from tests import HUNDREDS_DIRECTORY, PERMUTATION_DIRECTORY, _test_files

LANG = "uk"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("нуль", 0),
        ("нулю", 0),
        ("один", 1),
        ("одному", 1),
        ("одним", 1),
        ("одне", 1),
        ("одна", 1),
        ("одні", 1),
        ("два", 2),
        ("двох", 2),
        ("двум", 2),
        ("двоє", 2),
        ("три", 3),
        ("трьох", 3),
        ("троє", 3),
        ("чотири", 4),
        ("четверо", 4),
        ("пʼять", 5),
        ("пʼяти", 5),
        ("пʼятеро", 5),
        ("шість", 6),
        ("сім", 7),
        ("вісім", 8),
        ("девʼять", 9),
        ("десять", 10),
        ("одинадцять", 11),
        ("дванадцять", 12),
        ("тринадцять", 13),
        ("чотирнадцять", 14),
        ("пʼятнадцять", 15),
        ("шістнадцять", 16),
        ("сімнадцять", 17),
        ("вісімнадцять", 18),
        ("девʼятнадцять", 19),
        ("двадцять", 20),
        ("тридцять", 30),
        ("сорок", 40),
        ("пʼятдесят", 50),
        ("шістдесят", 60),
        ("сімдесят", 70),
        ("вісімдесят", 80),
        ("девʼяносто", 90),
        ("сто", 100),
        ("двісті", 200),
        ("триста", 300),
        ("чотириста", 400),
        ("пʼятсот", 500),
        ("шістсот", 600),
        ("сімсот", 700),
        ("вісімсот", 800),
        ("девʼятсот", 900),
        ("одна тисяча", 1000),
        ("одна тисяча один", 1001),
        ("одна тисяча два", 1002),
        ("одна тисяча три", 1003),
        ("одна тисяча чотири", 1004),
        ("одна тисяча пʼять", 1005),
        ("одна тисяча шість", 1006),
        ("одна тисяча сім", 1007),
        ("одна тисяча вісім", 1008),
        ("одна тисяча девʼять", 1009),
        ("одна тисяча десять", 1010),
        ("десять тисяч", 10000),
        ("сто тисяч", 100000),
        ("мільйон", 1_000_000),
        ("міліон", 1_000_000),
        ("один мільйон", 1000000),
        ("один мільйон один", 1000001),
        ("один мільйон два", 1000002),
        ("один мільйон три", 1000003),
        ("один мільйон чотири", 1000004),
        ("один мільйон пʼять", 1000005),
        ("десять мільйонів", 10000000),
        ("сто мільйонів", 100000000),
        ("мільярд", 1_000_000_000),
        ("один мільярд", 1000000000),
        ("один мільярд один", 1000000001),
        ("один мільярд два", 1000000002),
        ("один мільярд три", 1000000003),
        ("один мільярд чотири", 1000000004),
        ("один мільярд пʼять", 1000000005),
        ("десять мільярдів", 10000000000),
        ("сто мільярдів", 100000000000),
        ("трильйон", 1_000_000_000_000),
        ("один трильйон", 1000000000000),
        ("один трильйон один", 1000000000001),
        ("квадрильйон", 1_000_000_000_000_000),
        ("один квадрильйон", 1000000000000000),
        ("один квадрильйон один", 1000000000000001),
        ("квінтильйон", 1_000_000_000_000_000_000),
        ("секстильйон", 1_000_000_000_000_000_000_000),
        ("септильйон", 1_000_000_000_000_000_000_000_000),
        ("октильйон", 1_000_000_000_000_000_000_000_000_000),
        ("нонільйон", 1_000_000_000_000_000_000_000_000_000_000),
        ("децільйон", 1_000_000_000_000_000_000_000_000_000_000_000),
        ("ундецільйон", 1_000_000_000_000_000_000_000_000_000_000_000_000),
        ("дуодецільйон", 1_000_000_000_000_000_000_000_000_000_000_000_000_000),
        ("тредецільйон", 1_000_000_000_000_000_000_000_000_000_000_000_000_000_000),
        # Test cases with apostrophe
        ("п'ять", 5),
        ("п’ять", 5),
        ("п'ятдесят", 50),
        ("п’ятдесят", 50),
        ("п'ятисот", 500),
        ("п’ятисот", 500),
        ("п'ятнадцять", 15),
        ("п’ятнадцять", 15),
        ("п'ятдесят тисяч", 50_000),
        ("п’ятдесят тисяч", 50_000),
        ("дев'ять", 9),
        ("дев’ять", 9),
        ("дев'ятнадцять", 19),
        ("дев’ятнадцять", 19),
        ("дев'ятсот", 900),
        ("дев’ятсот", 900),
        ("дев'ятсот тисяч", 900_000),
        ("дев’ятсот тисяч", 900_000),
    ],
)
def test_parse_number(expected, test_input):
    assert parse_number(test_input, LANG) == expected


def test_parse_number_till_hundred():
    _test_files(HUNDREDS_DIRECTORY, LANG)


def test_parse_number_permutations():
    _test_files(PERMUTATION_DIRECTORY, LANG)
