import re
import string
# The initial global dictionaries that have been declared below will be changed,
# should be easily derived automatically from CLDR data/other source for each of the languages.

# We will need to have all values from 1-100 in a dictionary for some languages like hindi while others
# english / french build 2 digit numbers using MTEN dictionary values.
# (Difference observable in hi.json and en.json in numeral_language_data)

MULTIPLIERS = {
    "thousand": 1000,
    "thousands": 1000,
    "million": 1000000,
    "millions": 1000000,
    "billion": 1000000000,
    "billions": 1000000000,
    "trillion": 1000000000000,
    "trillions": 1000000000000,
}

# Would be language specific eg) 'et' in french
VALID_TOKENS_IN_NUMBERS = ["and", "-"]

UNITS = {
    word: value
    for value, word in enumerate(
        "one two three four five six seven eight nine".split(), 1
    )
}

STENS = {
    word: value
    for value, word in enumerate(
        "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(), 10
    )
}

MTENS = {
    word: value * 10
    for value, word in enumerate(
        "twenty thirty forty fifty sixty seventy eighty ninety".split(), 2
    )
}

HUNDRED = {"hundred": 100, "hundreds": 100}

ALL_WORDS = {**UNITS, **STENS, **MTENS, **HUNDRED, **MULTIPLIERS}
BASE_NUMBERS = {**UNITS, **STENS}

def check_validity(current_token, previous_token):
    if (current_token in BASE_NUMBERS):
        if previous_token in BASE_NUMBERS:
            return False

    if (current_token in MTENS):
        if (previous_token in MTENS) or (previous_token in BASE_NUMBERS):
            return False

    if (current_token in HUNDRED):
        if previous_token in MTENS:
            return False
    if (current_token in MULTIPLIERS):
        if previous_token in MULTIPLIERS:
            return False
    return True

def number_builder(token_list):
    total_value = 0
    current_grp_value = 0
    previous_token = None

    value_list = []

    for each_token in token_list:
        if each_token.isspace():
            continue
        valid = check_validity(each_token, previous_token)
        if not valid:
            total_value += current_grp_value
            value_list.append(str(total_value))
            total_value = 0
            current_grp_value = 0
            previous_token = None

        if (each_token in BASE_NUMBERS):
            current_grp_value += BASE_NUMBERS[each_token]

        if (each_token in MTENS):
            current_grp_value += MTENS[each_token]

        if (each_token in HUNDRED):
            if current_grp_value == 0:
                current_grp_value = 1
            current_grp_value *= 100

        if (each_token in MULTIPLIERS):
            if current_grp_value == 0:
                current_grp_value = 1

            current_grp_value *= MULTIPLIERS[each_token]
            total_value += current_grp_value
            current_grp_value = 0

        previous_token = each_token

    total_value += current_grp_value
    if total_value != 0:
        value_list.append(str(total_value))
    return value_list

# This has been structured to work for a string containing both words and numbers.
# eg) I have eight dollars -> I have 8 dollars.
# Currently it just takes word as numbers for inputs and translates them eight -> 8.
# Also the error handling etc needs to be taken care of.

SENTENCE_SEPERATORS = [".", ","]

def tokeniser(input_string):
    all_tokens = re.split(r'(\W)', input_string)
    return all_tokens

def parse_number(input_string):
    if input_string.isnumeric():
        return int(input_string)

    all_tokens = tokeniser(input_string)
    for index, each_token in enumerate(all_tokens):
        compare_token = each_token.lower()
        if compare_token in ALL_WORDS or compare_token.isspace():
            continue
        if (compare_token in VALID_TOKENS_IN_NUMBERS) and (index != 0):
            continue
        return None

    number_built = number_builder(all_tokens)
    if len(number_built) == 1:
        return int(number_built[0])
    return None

def parse(input_string):
    all_tokens = tokeniser(input_string)
    if all_tokens is None:
        return None

    final_sentence = []
    current_sentence = []
    tokens_taken = []

    for each_token in all_tokens:
        compare_token = each_token.lower()
        if (compare_token.isspace() or compare_token == ""):
            # Ignoring whitespace characters that are there when a number is being build.
            # eg) 'twenty     two' is same as 'twenty two'
            if not tokens_taken:
                current_sentence.append(each_token)
            continue

        if compare_token in SENTENCE_SEPERATORS:
            if tokens_taken:
                myvalue = number_builder(tokens_taken)
                for each_number in myvalue:
                    current_sentence.append(each_number)
                    current_sentence.append(" ")
                current_sentence.pop()
            current_sentence.append(each_token)
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
            current_sentence.append(each_token)

    if tokens_taken:
        myvalue = number_builder(tokens_taken)
        for each_number in myvalue:
            current_sentence.append(each_number)
            current_sentence.append(" ")

    final_sentence.extend(current_sentence)

    # Removing any trailing whitespaces added.
    output_string = ''.join(final_sentence).strip()
    return output_string
