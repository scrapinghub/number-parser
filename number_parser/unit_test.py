import unittest
import parser

class TestNumberParser(unittest.TestCase):
    def test_positives(self):
        self.assertEqual(parser.tokeniser("two million three thousand nine hundred and eighty four"), 2003984)
        self.assertEqual(parser.tokeniser("nineteen"), 19)
        self.assertEqual(parser.tokeniser("two thousand and nineteen"), 2019)
        self.assertEqual(parser.tokeniser("two million three thousand and nineteen"), 2003019)
        self.assertEqual(parser.tokeniser('three billion'), 3000000000)
        self.assertEqual(parser.tokeniser('three million'), 3000000)
        self.assertEqual(parser.tokeniser('one hundred twenty three million four hundred fifty six thousand seven hundred and eighty nine')
, 123456789)
        self.assertEqual(parser.tokeniser('eleven'), 11)
        self.assertEqual(parser.tokeniser('nineteen billion and nineteen'), 19000000019)
        self.assertEqual(parser.tokeniser('one hundred and forty two'), 142)
        self.assertEqual(parser.tokeniser('two million twenty three thousand and forty nine'), 2023049)
        self.assertEqual(parser.tokeniser('hundred'), 100)
        self.assertEqual(parser.tokeniser('thousand'), 1000)
        self.assertEqual(parser.tokeniser('million'), 1000000)
        self.assertEqual(parser.tokeniser('billion'), 1000000000)

if __name__ == '__main__':
    unittest.main()
