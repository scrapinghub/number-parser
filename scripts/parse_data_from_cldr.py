"""
The raw CLDR data was retreived on 25th Jun , 2020 from the following link
https://github.com/unicode-cldr/cldr-rbnf
"""

import os
import json
import re

SOURCE_PATH = "../number_parser_data/raw_cldr_translation_data/"
SUPPLEMENTARY_PATH = "../number_parser_data/supplementary_translation_data/"
TARGET_PATH = "../number_parser/data/"

VALID_KEYS = ["spellout-cardinal", "spellout-numbering"]
CAPTURE_BRACKET_CONTENT = r'\{(.*?)\}'
REQUIRED_DATA_POINTS = ["UNIT_NUMBERS", "BASE_NUMBERS", "MTENS", "MHUNDREDS", "MULTIPLIERS", "VALID_TOKENS"]


def _is_valid(key):
    for valid_key in VALID_KEYS:
        if valid_key in key:
            return True
    return False


def _parse_base_words(number, word, language_data):
    if number <= 9:
        language_data["UNIT_NUMBERS"][word] = number
    elif number <= 99:
        language_data["BASE_NUMBERS"][word] = number


def _find_zeroes(number):
    zero_count = 0
    while(number > 0):
        if number % 10 == 0:
            zero_count += 1
            number /= 10
        else:
            break
    return zero_count


def _parse_compound_words(number, word, language_data):
    power_of_10 = _find_zeroes(number)
    first_dig = str(number)[0]
    if power_of_10 == 0 or first_dig == '1':
        return

    root_word = word.split("[")[0]
    if power_of_10 == 1:
        language_data["MTENS"][root_word] = number
    elif power_of_10 == 2:
        language_data["MHUNDREDS"][root_word] = number


def _parse_multiplier_words(number, word, language_data):
    required_part = word.split("<")[-1]
    if required_part[0] != " ":
        return

    power_of_10 = _find_zeroes(number)
    if '$' in required_part:
        valid_words = re.findall(CAPTURE_BRACKET_CONTENT, required_part)
        for valid_word in valid_words:
            power_of_10_num = pow(10, power_of_10)
            if power_of_10 >= 2:
                language_data["MULTIPLIERS"][valid_word] = power_of_10_num

    else:
        valid_word = required_part.split("[")[0].strip()
        power_of_10_num = pow(10, power_of_10)
        if power_of_10 >= 2:
            language_data["MULTIPLIERS"][valid_word] = power_of_10_num


def _extract_information(key, word, language_data):
    try:
        number = int(key)
        word = word.replace(";", '')
        count_greater_than_sign = word.count('>')
        count_less_than_sign = word.count('<')
        count_equal_to_sign = word.count('=')
        if count_equal_to_sign != 0:
            return

        if count_greater_than_sign == 0 and count_less_than_sign == 0:
            _parse_base_words(number, word, language_data)
        elif count_greater_than_sign == 2 and count_less_than_sign == 0:
            _parse_compound_words(number, word, language_data)
        elif count_greater_than_sign == 2 and count_less_than_sign == 2:
            _parse_multiplier_words(number, word, language_data)

    except ValueError:
        print("The given key {} is not an integer".format(key))


def write_complete_data():
    for files in os.listdir(SOURCE_PATH):
        full_source_path = os.path.join(SOURCE_PATH, files)
        full_target_path = os.path.join(TARGET_PATH, files.split(".")[0]+".py")
        full_supplementary_path = os.path.join(SUPPLEMENTARY_PATH, files)

        language_data_populated = {}

        with open(full_source_path, 'r') as source:
            language_data = {}
            for keys in REQUIRED_DATA_POINTS:
                language_data[keys] = {}

            data = json.load(source)
            try:
                requisite_data = data['rbnf']['rbnf']['SpelloutRules']
            except KeyError:
                print("This key doesn't exist in {}".format(files))
                continue

            for keys, vals in requisite_data.items():
                if(_is_valid(keys)):
                    for key, val in vals.items():
                        _extract_information(key, val, language_data)

            language_data_populated = language_data

        with open(full_supplementary_path, 'r') as supplement:
            data = json.load(supplement)
            for keys in REQUIRED_DATA_POINTS:
                language_data_populated[keys].update(data[keys])

        encoding_comment = "# -*- coding: utf-8 -*-\n"
        translation_data = json.dumps(language_data_populated, indent=4, ensure_ascii=False)
        out_text = (encoding_comment + 'info = ' + translation_data + '\n').encode('utf-8')
        with open(full_target_path, 'wb+') as target_file:
            target_file.write(out_text)


if __name__ == '__main__':
    write_complete_data()
