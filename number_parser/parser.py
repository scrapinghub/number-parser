import re
import string
import os
import json
# The initial global dictionaries that have been declared below will be changed,
# should be easily derived automatically from CLDR data/other source for each of the languages.

# We will need to have all values from 1-100 in a dictionary for some languages like hindi while others
# english / french build 2 digit numbers using MTEN dictionary values.
# (Difference observable in hi.json and en.json in numeral_language_data)

LANGUAGE_DIRECTORY = "../number_parser/translation_data_merged/"
UNIT_NUMBERS = {}
BASE_NUMBERS = {}
MTENS = {}
MHUNDREDS = {}
MULTIPLIERS = {}
VALID_TOKENS_IN_NUMBERS = []
ALL_WORDS = {}
ALL_BASE_WORDS = {}

def populate_dictionaries(lang):
    file_name = lang + ".json"
    fpath = os.path.join(LANGUAGE_DIRECTORY, file_name)

    with open(fpath, 'r') as lang_file:
        lang_data = json.load(lang_file)
        unit_numbers = lang_data["UNIT_NUMBERS"]
        base_numbers = lang_data["BASE_NUMBERS"]
        mtens = lang_data["MTENS"]
        mhundreds = lang_data["MHUNDREDS"]
        multipliers = lang_data["MULTIPLIERS"]
        valid_tokens_in_numbers = lang_data["VALID_TOKENS"]["tokens"]
        all_words = {**unit_numbers, **base_numbers, **mtens, **mhundreds, **multipliers}
        all_base_words = {**unit_numbers, **base_numbers}

        UNIT_NUMBERS.update(unit_numbers)
        BASE_NUMBERS.update(base_numbers)
        MTENS.update(mtens)
        MHUNDREDS.update(mhundreds)
        MULTIPLIERS.update(multipliers)
        ALL_WORDS.update(all_words)
        ALL_BASE_WORDS.update(all_base_words)
        VALID_TOKENS_IN_NUMBERS[:] = valid_tokens_in_numbers

def check_validity(current_token, previous_token):
    """Identifies whether the new token can continue building the previous number."""
    if current_token in ALL_BASE_WORDS and previous_token in ALL_BASE_WORDS:
        return False

    if current_token in BASE_NUMBERS and previous_token in MTENS:
        return False

    elif (current_token in MTENS):
        if (previous_token in MTENS) or (previous_token in ALL_BASE_WORDS):
            return False

    elif (current_token in MHUNDREDS):
        if previous_token not in MULTIPLIERS and previous_token is not None:
            return False

    elif (current_token in MULTIPLIERS and previous_token in MULTIPLIERS):
        if MULTIPLIERS[current_token] > MULTIPLIERS[previous_token]:
            return False

    return True

def number_builder(token_list):
    """Incrementaly builds a number from the list of tokens."""
    total_value = 0
    current_grp_value = 0
    previous_token = None
    value_list = []

    for token in token_list:
        if token.isspace():
            continue
        valid = check_validity(token, previous_token)
        if not valid:
            total_value += current_grp_value
            value_list.append(str(total_value))
            total_value = 0
            current_grp_value = 0
            previous_token = None

        if (token in ALL_BASE_WORDS):
            current_grp_value += ALL_BASE_WORDS[token]

        elif (token in MTENS):
            current_grp_value += MTENS[token]

        elif (token in MHUNDREDS):
            current_grp_value += MHUNDREDS[token]

        elif (token in MULTIPLIERS):
            if current_grp_value == 0:
                current_grp_value = 1

            if MULTIPLIERS[token] == 100:
                current_grp_value *= MULTIPLIERS[token]
            else:
                current_grp_value *= MULTIPLIERS[token]
                total_value += current_grp_value
                current_grp_value = 0

        previous_token = token

    total_value += current_grp_value
    value_list.append(str(total_value))
    return value_list

SENTENCE_SEPERATORS = [".", ","]

def tokenize(input_string):
    """Breaks string on any non-word character."""
    tokens = re.split(r'(\W)', input_string)
    return tokens

def parse_number(input_string, lang='en'):
    populate_dictionaries(lang)
    """Converts a single number written in natural language to a numeric type"""
    if input_string.isnumeric():
        return int(input_string)

    tokens = tokenize(input_string)

    for index, token in enumerate(tokens):
        compare_token = token.lower()
        if compare_token in ALL_WORDS or compare_token.isspace() or len(compare_token) == 0:
            continue
        if (compare_token in VALID_TOKENS_IN_NUMBERS) and (index != 0):
            continue
        return None

    number_built = number_builder(tokens)
    if len(number_built) == 1:
        return int(number_built[0])
    return None

def parse(input_string, lang='en'):
    """
    Converts all the numbers in a sentence written in natural language to their numeric type while keeping
    the other words unchanged. Returns the transformed string.
    """
    populate_dictionaries(lang)
    tokens = tokenize(input_string)
    if tokens is None:
        return None

    final_sentence = []
    current_sentence = []
    tokens_taken = []

    for token in tokens:
        compare_token = token.lower()

        if (compare_token.isspace() or compare_token == ""):
            if not tokens_taken:
                current_sentence.append(token)
            continue

        if compare_token in SENTENCE_SEPERATORS:
            if tokens_taken:
                myvalue = number_builder(tokens_taken)
                for each_number in myvalue:
                    current_sentence.append(each_number)
                    current_sentence.append(" ")
                current_sentence.pop()
            current_sentence.append(token)
            final_sentence.extend(current_sentence)
            tokens_taken = []
            current_sentence = []
            continue

        if ((compare_token in ALL_WORDS) or (compare_token in VALID_TOKENS_IN_NUMBERS and len(tokens_taken) != 0)):
            tokens_taken.append(compare_token)

        else:
            if tokens_taken:
                myvalue = number_builder(tokens_taken)
                for each_number in myvalue:
                    current_sentence.append(each_number)
                    current_sentence.append(" ")
                tokens_taken = []
            current_sentence.append(token)

    if tokens_taken:
        myvalue = number_builder(tokens_taken)
        for each_number in myvalue:
            current_sentence.append(each_number)
            current_sentence.append(" ")

    final_sentence.extend(current_sentence)

    output_string = ''.join(final_sentence).strip()
    return output_string
