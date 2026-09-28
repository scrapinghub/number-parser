import pytest

from number_parser import parse, parse_number


@pytest.mark.parametrize(
    "test_input,expected,lang",
    [
        ("三", 3, None),
        ("百四十五", 145, None),
        ("十五", 15, "ja"),
        ("二千三百四十五", 2_345, "ja"),
        ("三万二千", 32_000, "ja"),
        ("一億二千万", 120_000_000, "ja"),
        ("九千九百九十九兆", 9_999_000_000_000_000, "ja"),
        ("十二万", 120_000, "zh"),
        ("一百零五", 105, "zh"),
        ("两千", 2_000, "zh"),
        ("壹佰贰拾叁", 123, "zh"),
        ("二〇二四", 2_024, "zh"),
        ("三千五百万亿", 3_500_000_000_000_000, "zh"),
        ("一万二千亿", 1_200_000_000_000, "zh"),
        ("萬", 10_000, "zh-Hant"),
        ("万万", None, "zh"),
    ],
)
def test_parse_number(expected, test_input, lang):
    assert parse_number(test_input, language=lang) == expected


@pytest.mark.parametrize(
    "test_input,expected,lang",
    [
        ("我有三百五十个苹果。", "我有350个苹果。", "zh"),
        ("二〇二四年三月十五日", "2024年3月15日", "zh"),
        ("価格は一万二千円です", "価格は12000円です", "ja"),
        ("一億五千萬人", "150000000人", "zh-Hant"),
    ],
)
def test_parse(expected, test_input, lang):
    assert parse(test_input, language=lang) == expected
