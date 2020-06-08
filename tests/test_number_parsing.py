from number_parser import parser

class TestNumberParser():
    def test_only_number(self):
        assert (parser.parser("two million three thousand nine hundred and eighty four") == "2003984")
        assert (parser.parser("nineteen") == "19")
        assert (parser.parser("two thousand and nineteen") == "2019")
        assert (parser.parser("two million three thousand and nineteen") == "2003019")
        assert (parser.parser('three billion') == "3000000000")
        assert (parser.parser('three million') == "3000000")
        assert (parser.parser('one hundred twenty three million four hundred fifty six thousand seven hundred and eighty nine') == "123456789")
        assert (parser.parser('eleven') == "11")
        assert (parser.parser('nineteen billion and nineteen') == "19000000019")
        assert (parser.parser('one hundred and forty two') == "142")
        assert (parser.parser('two million twenty three thousand and forty nine') == "2023049")
        assert (parser.parser('hundred') == "100")
        assert (parser.parser('thousand') == "1000")
        assert (parser.parser('million') == "1000000")
        assert (parser.parser('billion') == "1000000000")

    def test_basic_sentences(self):
        input = "twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes."
        expected = "25 cows, 12 chickens and 125 kg of potatoes."
        assert(parser.parser(input) == expected)

        input = "I have eight cows"
        expected = "I have 8 cows"
        assert(parser.parser(input) == expected)

        input = "I have eight cows three bulls and seven hundred and twelve million dollars "
        expected = "I have 8 cows 3 bulls and 712000000 dollars"
        assert(parser.parser(input) == expected)

        input = "They just won seventy-five thousand dollars"
        expected = "They just won 75000 dollars"
        assert(parser.parser(input) == expected)

        input = "I have eight cows. I don't have eighteen cows"
        expected = "I have 8 cows. I don't have 18 cows"
        assert(parser.parser(input) == expected)

        input = "thirty-four cows = thirty four cows"
        expected = "34 cows = 34 cows"
        assert(parser.parser(input) == expected)

        input = "thirty       four       cows = thirty four cows"
        expected = "34 cows = 34 cows"
        assert(parser.parser(input) == expected)

        input = "the     sun      is     hundred     and   twelve       km     away."
        expected = "the     sun      is     112 km     away."
        assert(parser.parser(input) == expected)

    def test_ambigous_sentences(self):
        input = "one two three four twenty five."
        expected = input
        assert(parser.parser(input) == expected)

        input = "one two three four twenty, five."
        expected = "one two three four twenty, 5."
        assert(parser.parser(input) == expected)
