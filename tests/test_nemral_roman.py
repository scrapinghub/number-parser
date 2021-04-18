import pytest
from number_parser import parse_roman


@pytest.mark.parametrize(
    "test_string, expected",
    [
        ('CDXX', '420'),
        ('lxix', '69'),
        ('Built in MMLXXVII', 'Built in 2077'),
    ]
)
def test_parse_roman(test_string, expected):
    assert parse_roman(test_string) == expected
