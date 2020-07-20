"""
The raw CLDR data was retreived on 25th Jun , 2020 from the following link
https://github.com/unicode-cldr/cldr-rbnf
"""

import os
import json
import re
from collections import OrderedDict

SOURCE_PATH = "../number_parser_data/raw_cldr_translation_data/"
SUPPLEMENTARY_PATH = "../number_parser_data/supplementary_translation_data/"
TARGET_PATH = "../number_parser/data/"

VALID_KEYS = ["spellout-cardinal", "spellout-numbering"]
INVALID_KEYS = ["cents"]
CAPTURE_BRACKET_CONTENT = r'\{(.*?)\}'
REQUIRED_NUMBERS_DATA = ["UNIT_NUMBERS", "DIRECT_NUMBERS", "TENS", "HUNDREDS", "BIG_POWERS_OF_TEN"]


def _is_valid(key):
    """Identifying whether the given key of the source language file needs to be extracted."""
    is_valid = False
    for valid_key in VALID_KEYS:
        if valid_key in key:
            is_valid = True
    for invalid_key in INVALID_KEYS:
        if invalid_key in key:
            is_valid = False
    return is_valid


def _add_base_words(number, word, language_data):
    """Adding basic two digit words - i.e words that are standalone numbers on their own."""
    if word == "ERROR" or word == "":
        return
    if number <= 9:
        language_data["UNIT_NUMBERS"][word] = number
    elif number <= 99:
        language_data["DIRECT_NUMBERS"][word] = number


def _count_zero(number):
    """Counting the number of zeroes in the given number."""
    zero_count = 0
    while number > 9:
        if number % 10 == 0:
            zero_count += 1
            number /= 10
        else:
            break
    return zero_count


def _add_compound_words(number, word, language_data):
    """Adding compound words - i.e words that may be used along with another word to form a number"""
    power_of_10 = _count_zero(number)
    first_dig = str(number)[0]
    if power_of_10 == 0 or first_dig == '1':
        return

    if "[" in word:
        root_word = word.split("[")[0].strip()
    else:
        root_word = word.split(">")[0].strip()

    if root_word == "":
        return

    if power_of_10 == 1:
        language_data["TENS"][root_word] = number
    elif power_of_10 == 2:
        language_data["HUNDREDS"][root_word] = number


def _add_multiplier_words(number, word, language_data):
    """Adding words that are large powers of 10 which are used to form bigger numbers."""
    required_part = word.split("<")[-1]
    if required_part[0] != " ":
        return

    power_of_10 = _count_zero(number)
    if '$' in required_part:
        valid_words = re.findall(CAPTURE_BRACKET_CONTENT, required_part)
        for valid_word in valid_words:
            power_of_10_num = pow(10, power_of_10)
            if power_of_10 >= 2:
                language_data["BIG_POWERS_OF_TEN"][valid_word] = power_of_10_num
        return
    if "[" in required_part:
        valid_word = required_part.split("[")[0].strip()
    else:
        valid_word = required_part.split(">")[0].strip()

    power_of_10_num = pow(10, power_of_10)
    if power_of_10 >= 2:
        language_data["BIG_POWERS_OF_TEN"][valid_word] = power_of_10_num


def _extract_information(key, word, language_data):
    """Identify the type of number - simple,compound,multiplier."""
    try:
        number = int(key)
    except ValueError:
        print("The given key {} is not an integer".format(key))
        return

    word = word.replace(";", '')
    count_greater_than_sign = word.count('>')
    count_less_than_sign = word.count('<')
    count_equal_to_sign = word.count('=')
    if count_equal_to_sign != 0:
        return
    if count_greater_than_sign == 0 and count_less_than_sign == 0:
        _add_base_words(number, word, language_data)
    elif count_greater_than_sign == 2 and count_less_than_sign == 0:
        _add_compound_words(number, word, language_data)
    elif count_greater_than_sign == 2 and count_less_than_sign == 2:
        _add_multiplier_words(number, word, language_data)


def write_complete_data():
    """
    Main function to extract data from source files , merge with supplementary data
    and write the combined results to the final target directory.
    """
    for file_name in os.listdir(SOURCE_PATH):
        full_source_path = os.path.join(SOURCE_PATH, file_name)
        full_target_path = os.path.join(TARGET_PATH, file_name.split(".")[0]+".py")
        full_supplementary_path = os.path.join(SUPPLEMENTARY_PATH, file_name)

        language_data = {key: {} for key in REQUIRED_NUMBERS_DATA}
        ordered_language_data = OrderedDict((key, {}) for key in REQUIRED_NUMBERS_DATA)
        with open(full_source_path, 'r') as source:
            data = json.load(source)
            try:
                requisite_data = data['rbnf']['rbnf']['SpelloutRules']
            except KeyError:
                print("This key doesn't exist in {}".format(file_name))
                continue

            for keys, vals in requisite_data.items():
                if _is_valid(keys):
                    for key, val in vals.items():
                        # Removing soft-hyphens from the source file.
                        val = val.replace('\xad', '')
                        _extract_information(key, val, language_data)

        with open(full_supplementary_path, 'r') as supplementary_data:
            data = json.load(supplementary_data)
            for keys in REQUIRED_NUMBERS_DATA:
                language_data[keys].update(data[keys])
                sorted_tuples = sorted(language_data[keys].items(), key=lambda x: (x[1], x[0]))
                for items in sorted_tuples:
                    word, number = items[0], items[1]
                    ordered_language_data[keys][word] = int(number)
            skip_tokens = sorted(data["SKIP_TOKENS"])
        ordered_language_data["SKIP_TOKENS"] = skip_tokens
        translation_data = json.dumps(ordered_language_data, indent=4, ensure_ascii=False)
        out_text = ('info = ' + translation_data + '\n')
        with open(full_target_path, 'w+') as target_file:
            target_file.write(out_text)


if __name__ == '__main__':
    write_complete_data()
