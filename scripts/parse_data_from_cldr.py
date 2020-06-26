import os
import json
from pprint import pprint
import re

SOURCE_PATH = "../raw_cldr_translation_data/"
TARGET_PATH = "../number_parser/translation_data_merged"
SUPPLEMENTARY_PATH = "../supplementary_translation_data/"

REQUIRED_KEYS = ["spellout-cardinal", "spellout-numbering"]
CAPTURE_BRACKET_CONTENT = r'\{(.*?)\}'

LARGE_EXCEPTIONS = {}

UNIT_NUMBERS = {}
BASE_NUMBERS = {}
MTENS = {}
MHUNDREDS = {}
MULTIPLIERS = {}
VALID_TOKENS = {}

def is_valid(key):
    for each in REQUIRED_KEYS:
        if each in key:
            return True
    return False

def parse_base_words(number, word):
    if number <= 9:
        UNIT_NUMBERS[word] = number
    elif number <= 99:
        BASE_NUMBERS[word] = number
    else:
        LARGE_EXCEPTIONS[word] = number

def find_zeroes(number):
    zero_count = 0
    while(number > 0):
        if number % 10 == 0:
            zero_count += 1
            number /= 10
        else:
            break
    return zero_count

def parse_compound_words(number, word):
    power_of_10 = find_zeroes(number)
    first_dig = str(number)[0]
    if power_of_10 == 0 or first_dig == '1':
        return

    root_word = word.split("[")[0]
    if power_of_10 == 1:
        MTENS[root_word] = number
    else:
        MHUNDREDS[root_word] = number

def parse_multiplier_words(number,word):
    required_part = word.split("<")[-1]
    if required_part[0] != " ":
        return

    power_of_10 = find_zeroes(number)
    if '$' in required_part:
        valid_words = re.findall(CAPTURE_BRACKET_CONTENT, required_part)
        for valid_word in valid_words:
            power_of_10_num = pow(10, power_of_10)
            if power_of_10 >= 2:
                MULTIPLIERS[valid_word] = power_of_10_num

    else:
        valid_word = required_part.split("[")[0].strip()
        power_of_10_num = pow(10, power_of_10)
        if power_of_10 >= 2:
            MULTIPLIERS[valid_word] = power_of_10_num

def extract_information(key, word):
    try:
        number = int(key)
        word = word.replace(";", '')
        count_greater_than_sign = word.count('>')
        count_less_than_sign = word.count('<')
        count_equal_to_sign = word.count('=')
        if count_equal_to_sign != 0:
            return

        if count_greater_than_sign == 0 and count_less_than_sign == 0:
            parse_base_words(number, word)
        elif count_greater_than_sign == 2 and count_less_than_sign == 0:
            parse_compound_words(number, word)
        elif count_greater_than_sign == 2 and count_less_than_sign == 2:
            parse_multiplier_words(number, word)

    except:
        pass

for files in os.listdir(SOURCE_PATH):
    full_source_path = os.path.join(SOURCE_PATH, files)
    full_target_path = os.path.join(TARGET_PATH, files)
    full_supplementary_path = os.path.join(SUPPLEMENTARY_PATH, files)

    with open(full_source_path, 'r') as source:
        data = json.load(source)
        try:
            requisite_data = data['rbnf']['rbnf']['SpelloutRules']
        except Exception as e:
            print(e)
            continue

        for keys, vals in requisite_data.items():
            if(is_valid(keys)):
                for key, val in vals.items():
                    extract_information(key, val)

    with open(full_supplementary_path,'r') as supplement:
        data = json.load(supplement)

        unit_numbers = data["UNIT_NUMBERS"]
        base_numbers = data["BASE_NUMBERS"]
        mtens = data["MTENS"]
        mhundreds = data["MHUNDREDS"]
        multipliers = data["MULTIPLIERS"]
        valid_tokens = data["VALID_TOKENS"]

        UNIT_NUMBERS.update(unit_numbers)
        BASE_NUMBERS.update(base_numbers)
        MTENS.update(mtens)
        MHUNDREDS.update(mhundreds)
        MULTIPLIERS.update(multipliers)
        VALID_TOKENS.update(valid_tokens)

    list_of_numbers = {}

    list_of_numbers["UNIT_NUMBERS"] = UNIT_NUMBERS
    list_of_numbers["BASE_NUMBERS"] = BASE_NUMBERS
    list_of_numbers["MTENS"] = MTENS
    list_of_numbers["MHUNDREDS"] = MHUNDREDS
    list_of_numbers["MULTIPLIERS"] = MULTIPLIERS
    list_of_numbers["VALID_TOKENS"] = VALID_TOKENS

    full_target_path = os.path.join(TARGET_PATH, files)

    with open(full_target_path, 'w+') as target:
        json.dump(list_of_numbers, target, indent=4, ensure_ascii=False)

    UNIT_NUMBERS = {}
    BASE_NUMBERS = {}
    MTENS = {}
    MHUNDREDS = {}
    MULTIPLIERS = {}
    VALID_TOKENS = {}
