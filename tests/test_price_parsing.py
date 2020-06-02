import pytest
from number_parser import parser

class TestNumberParser():
    def basic_test(self):
        assert parser.tokeniser("two million three thousand nine hundred and eighty four") == 2003984
        assert parser.tokeniser("nineteen") == 19
        assert parser.tokeniser("two thousand and nineteen") == 2019
        assert parser.tokeniser("two million three thousand and nineteen") == 2003019
        assert parser.tokeniser('three billion') == 3000000000
        assert parser.tokeniser('three million') == 3000000
        assert parser.tokeniser('one hundred twenty three million four hundred fifty six thousand seven hundred and eighty nine')
, 123456789)
        assert parser.tokeniser('eleven') == 11
        assert parser.tokeniser('nineteen billion and nineteen') == 19000000019
        assert parser.tokeniser('one hundred and forty two') == 142
        assert parser.tokeniser('two million twenty three thousand and forty nine') == 2023049
        assert parser.tokeniser('hundred') == 100
        assert parser.tokeniser('thousand') == 1000
        assert parser.tokeniser('million') == 1000000
        assert parser.tokeniser('billion') == 1000000000