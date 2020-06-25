import os
import json
from pprint import pprint
import re

ROOT_PATH = "../numeral_translation_data/raw_cldr_translation_data/"
REQUIRED_KEYS = ["spellout-cardinal", "spellout-numbering"]
CAPTURE_BRACKET_CONTENT = r'\{(.*?)\}'

LARGE_EXCEPTIONS = {}

UNIT_NUMBERS = {}
BASE_NUMBERS = {}
MTENS = {}

MHUNDREDS = {}

HUNDREDS_MULTIPLIER = {}
MULTIPLIERS = {}

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
            if power_of_10 == 2:
                HUNDREDS_MULTIPLIER[valid_word] = power_of_10_num
            else:
                MULTIPLIERS[valid_word] = power_of_10_num

    else:
        valid_word = required_part.split("[")[0].strip()
        power_of_10_num = pow(10, power_of_10)

        if power_of_10 == 2:
            HUNDREDS_MULTIPLIER[valid_word] = power_of_10_num
        else:
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

for files in os.listdir(ROOT_PATH):
    full_path = os.path.join(ROOT_PATH, files)
    if (files != 'ru.json'):
        continue

    with open(full_path, 'r') as source:
        data = json.load(source)
        requisite_data = data['rbnf']['rbnf']['SpelloutRules']
        for keys, vals in requisite_data.items():
            if(is_valid(keys)):
                for key, val in vals.items():
                    extract_information(key, val)
    # break
    print(UNIT_NUMBERS)
    print("----")
    print(BASE_NUMBERS)
    print("----")
    print(MTENS)
    print("----")
    print(MHUNDREDS)
    print("----")
    print(HUNDREDS_MULTIPLIER)
    print("----")
    print(MULTIPLIERS)
    BASE_NUMBERS = {}
