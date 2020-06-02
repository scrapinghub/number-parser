import re

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
VALID_WORDS_IN_NUMBERS = ["and"]

UNITS = {
word: value
for value, word in enumerate(
    "one two three four five six seven eight nine".split(),1
    )
}

STENS = {
word: value
for value, word in enumerate(
    "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(),10
    )
}

MTENS = {
    word: value * 10
    for value, word in enumerate(
        "twenty thirty forty fifty sixty seventy eighty ninety".split(),2
    )
}

HUNDRED = {"hundred": 100, "hundreds": 100}

ALL_WORDS = {**UNITS , **STENS , **MTENS, **HUNDRED, **MULTIPLIERS}

def handle_single_words(token_list):
    word = token_list[0]
    if word in ALL_WORDS:
        return ALL_WORDS[word]

def number_builder(token_list):

    if len(token_list) == 1:
        return handle_single_words(token_list)

    total_value = 0
    current_grp_value = 0

    previous_base_word = False
    previous_multiplier_word = False
    previous_mtens_word = False
    ## To-Do simplify logic by changing this maintenance of 3 variable to `1` (previous token value perhaps ?)

    for each_token in token_list:
        if ( each_token in UNITS):
            if previous_base_word:
                return ValueError
            current_grp_value += UNITS[each_token]
            previous_base_word = True
            previous_multiplier_word = False

        if ( each_token in STENS):
            current_grp_value += STENS[each_token]
            if previous_base_word:
                return ValueError
            previous_base_word = True
            previous_multiplier_word = False

        if ( each_token in MTENS):
            if previous_mtens_word:
                return ValueError
            previous_mtens_word = True
            previous_base_word = False
            previous_multiplier_word = False
            current_grp_value += MTENS[each_token]

        if ( each_token in HUNDRED):
            current_grp_value *= 100
            previous_base_word = False
            previous_multiplier_word = False
            previous_mtens_word = False

        if  (each_token in MULTIPLIERS):
            if previous_multiplier_word:
                return ValueError
            current_grp_value *= MULTIPLIERS[each_token]
            total_value += current_grp_value
            current_grp_value = 0
            previous_base_word = False
            previous_mtens_word = False
            previous_multiplier_word = True


    total_value += current_grp_value
    return total_value

# This has been structured to work for a string containing both words and numbers.
# eg) I have eight dollars -> I have 8 dollars.
# Currently it just takes word as numbers for inputs and translates them eight -> 8.
# Also the error handling etc needs to be taken care of.

def parser(input_stream):
    # comma seperated or full stop for different sentences.
    input_stream = input_stream.lower()
    sentences = re.split('[.,]',input_stream)

    for each_sentence in sentences:
        tokens_taken = []
        each_sentence = each_sentence.strip()
        all_vals = re.split('\W+',each_sentence)
        for each_token in all_vals:
            if ( (each_token in UNITS)
            or (each_token in STENS)
            or (each_token in MTENS)
            or (each_token in MULTIPLIERS)
            or ( (each_token in VALID_WORDS_IN_NUMBERS) and len(tokens_taken) != 0)
            or (each_token in HUNDRED) ):
                tokens_taken.append(each_token)

            else:
                myvalue = number_builder(tokens_taken)
                tokens_taken = []
                return myvalue

        if tokens_taken is not None:
            myvalue = number_builder(tokens_taken)
            return myvalue