import re
from importlib import import_module
SENTENCE_SEPERATORS = [".", ","]


class Language:
    """Main language class to populate the requisite language-specific variables."""
    unit_numbers = {}
    direct_numbers = {}
    tens = {}
    hundreds = {}
    big_powers_of_ten = {}
    skip_tokens = []
    all_numbers = {}
    unit_and_direct_numbers = {}

    def __init__(self, lang):
        language_info = getattr(import_module('number_parser.data.' + lang), 'info')
        self.unit_numbers = language_info["UNIT_NUMBERS"]
        self.direct_numbers = language_info["DIRECT_NUMBERS"]
        self.tens = language_info["TENS"]
        self.hundreds = language_info["HUNDREDS"]
        self.big_powers_of_ten = language_info["BIG_POWERS_OF_TEN"]
        self.skip_tokens = language_info["SKIP_TOKENS"]

        self.all_numbers = {**self.unit_numbers, **self.direct_numbers, **self.tens,
                            **self.hundreds, **self.big_powers_of_ten}
        self.unit_and_direct_numbers = {**self.unit_numbers, **self.direct_numbers}


def _check_validity(current_token, previous_token, lang):
    """Identifies whether the new token can continue building the previous number."""
    if current_token in lang.unit_and_direct_numbers and previous_token in lang.unit_and_direct_numbers:
        return False

    if current_token in lang.direct_numbers and previous_token in lang.tens:
        return False

    elif current_token in lang.tens:
        if previous_token in lang.tens or previous_token in lang.unit_and_direct_numbers:
            return False

    elif current_token in lang.hundreds:
        if previous_token not in lang.big_powers_of_ten and previous_token is not None:
            return False

    elif current_token in lang.big_powers_of_ten and previous_token in lang.big_powers_of_ten:
        if lang.big_powers_of_ten[current_token] > lang.big_powers_of_ten[previous_token]:
            return False

    return True


def _number_builder(token_list, lang):
    """Incrementaly builds a number from the list of tokens."""
    total_value = 0
    current_grp_value = 0
    previous_token = None
    value_list = []

    for token in token_list:
        if token.isspace():
            continue
        valid = _check_validity(token, previous_token, lang)
        if not valid:
            total_value += current_grp_value
            value_list.append(str(total_value))
            total_value = 0
            current_grp_value = 0
            previous_token = None

        if token in lang.unit_and_direct_numbers:
            current_grp_value += lang.unit_and_direct_numbers[token]

        elif token in lang.tens:
            current_grp_value += lang.tens[token]

        elif token in lang.hundreds:
            current_grp_value += lang.hundreds[token]

        elif token in lang.big_powers_of_ten:
            if current_grp_value == 0:
                current_grp_value = 1

            if lang.big_powers_of_ten[token] == 100:
                current_grp_value *= lang.big_powers_of_ten[token]
            else:
                current_grp_value *= lang.big_powers_of_ten[token]
                total_value += current_grp_value
                current_grp_value = 0

        previous_token = token

    total_value += current_grp_value
    value_list.append(str(total_value))
    return value_list


def _tokenize(input_string):
    """Breaks string on any non-word character."""
    tokens = re.split(r'(\W)', input_string)
    return tokens


def parse_number(input_string, language='en'):
    """Converts a single number written in natural language to a numeric type"""
    lang = Language(language)
    if input_string.isnumeric():
        return int(input_string)

    tokens = _tokenize(input_string)

    for index, token in enumerate(tokens):
        compare_token = token.lower()
        if compare_token in lang.all_numbers or compare_token.isspace() or len(compare_token) == 0:
            continue
        if compare_token in lang.skip_tokens and index != 0:
            continue
        return None

    number_built = _number_builder(tokens, lang)
    if len(number_built) == 1:
        return int(number_built[0])
    return None


def parse(input_string, language='en'):
    """
    Converts all the numbers in a sentence written in natural language to their numeric type while keeping
    the other words unchanged. Returns the transformed string.
    """
    lang = Language(language)
    tokens = _tokenize(input_string)
    if tokens is None:
        return None

    final_sentence = []
    current_sentence = []
    tokens_taken = []

    for token in tokens:
        compare_token = token.lower()

        if compare_token.isspace() or compare_token == "":
            if not tokens_taken:
                current_sentence.append(token)
            continue

        if compare_token in SENTENCE_SEPERATORS:
            if tokens_taken:
                myvalue = _number_builder(tokens_taken, lang)
                for each_number in myvalue:
                    current_sentence.append(each_number)
                    current_sentence.append(" ")
                current_sentence.pop()
            current_sentence.append(token)
            final_sentence.extend(current_sentence)
            tokens_taken = []
            current_sentence = []
            continue

        if (compare_token in lang.all_numbers) or (compare_token in lang.skip_tokens and len(tokens_taken) != 0):
            tokens_taken.append(compare_token)

        else:
            if tokens_taken:
                myvalue = _number_builder(tokens_taken, lang)
                for each_number in myvalue:
                    current_sentence.append(each_number)
                    current_sentence.append(" ")
                tokens_taken = []
            current_sentence.append(token)

    if tokens_taken:
        myvalue = _number_builder(tokens_taken, lang)
        for each_number in myvalue:
            current_sentence.append(each_number)
            current_sentence.append(" ")

    final_sentence.extend(current_sentence)

    output_string = ''.join(final_sentence).strip()
    return output_string
