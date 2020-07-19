import pytest
from number_parser import parse
LANG = 'en'


class TestNumberParser():
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("OnE DaY at a Time.", "1 DaY at a Time."),
            ("SeVentY THREE days of SUMMER!!!.", "73 days of SUMMER!!!."),
            ("Twelve 11 pm", "12 11 pm"),
        ]
    )
    def test_parse_case_of_string(self, expected, test_input):
        assert parse(test_input, LANG) == expected
