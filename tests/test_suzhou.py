import pytest

from number_parser import parse, parse_number


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("〤", 4),
        ("〤〇〢", 402),
        (" 〩〨〧 ", 987),
        ("〡一", 11),
        ("二〢", 22),
        ("〸", 10),
        ("〺", 30),
    ],
)
def test_parse_number(test_input, expected):
    assert parse_number(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("价格〤〇〢元", "价格402元"),
        ("〡一 and two", "11 and 2"),
        ("第〹号", "第20号"),
        ("三〇", "三〇"),
        ("〸〡", "〸〡"),
    ],
)
def test_parse(test_input, expected):
    assert parse(test_input) == expected


def test_parse_types():
    assert parse("〤〇〢 and two", types={"cardinal"}) == "〤〇〢 and 2"
