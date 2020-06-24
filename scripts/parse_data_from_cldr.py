import os
import json
from pprint import pprint

ROOT_PATH = "../numeral_translation_data/"
REQUIRED_KEYS = ["spellout-cardinal", "spellout-numbering"]


BASE_NUMBERS = {}
MTENS = {}

HUNDRED_BASE_NUMBERS = {}

HUNDRED_MULTIPLIERS = {}
MULTIPLIERS = {}


def is_valid(key):
    for each in REQUIRED_KEYS:
        if each in key:
            return True
    return False

def parse_base_words(number, word):
    BASE_NUMBERS[word] = number

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
    if power_of_10 == 0:
        return

    root_word = word.split("[")[0]
    print(number,root_word)




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
            parse_base_words(number,word)
        elif count_greater_than_sign == 2 and count_less_than_sign == 0:
            parse_compound_words(number,word)

    except:
        pass

for files in os.listdir(ROOT_PATH):
    full_path = os.path.join(ROOT_PATH, files)
    if (files != 'fr.json'):
        continue

    with open(full_path, 'r') as source:
        data = json.load(source)
        requisite_data = data['rbnf']['rbnf']['SpelloutRules']
        for keys, vals in requisite_data.items():
            if(is_valid(keys)):
                for key, val in vals.items():
                    extract_information(key, val)
    # print(BASE_NUMBERS)
    break
    BASE_NUMBERS = {}
