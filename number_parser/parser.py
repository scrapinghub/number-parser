import re

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

def number_builder(token_list):
    total_value = 0
    current_grp_value = 0

    previous_base_word = False
    previous_multiplier_word = False
    previous_mtens_word = False
    ## To-Do Change this maintenance of 3 variable to `1` (prevtoken type)
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

        # print(total_value)

    total_value += current_grp_value
    return total_value

def tokeniser(input_stream):

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
            or (each_token in VALID_WORDS_IN_NUMBERS)
            or (each_token in HUNDRED) ):
                tokens_taken.append(each_token)
            else:
                myvalue = number_builder(tokens_taken)
                tokens_taken = []
                print(myvalue)

        if tokens_taken is not None:
            myvalue = number_builder(tokens_taken)
            print(myvalue)
    # segments = re.split(r"\s*[\.,;\(\)…\[\]:!\?]+\s*", input_stream)
    # punct = re.findall(r"\s*[\.,;\(\)…\[\]:!\?]+\s*", input_stream)
    # print(segments)

tokeniser("two million three thousand nine hundred and eighty four")
tokeniser("nineteen")
tokeniser("two thousand and nineteen")
tokeniser("two million three thousand and nineteen")
tokeniser('three billion')
tokeniser('three million')
tokeniser('one hundred twenty three million four hundred fifty six thousand seven hundred and eighty nine')
tokeniser('eleven')
tokeniser('nineteen billion and nineteen')
tokeniser('one hundred and forty two')
tokeniser('five')
tokeniser('two million twenty three thousand and forty nine')
tokeniser('two point three')
tokeniser('two million twenty three thousand and forty nine')
tokeniser('one billion two million twenty three thousand and forty nine')
tokeniser('one hundred thirty-five')
tokeniser('hundred')
tokeniser('thousand')
tokeniser('million')
tokeniser('billion')
tokeniser('nineteen hundred seventy-three')
tokeniser('thousand thousand two hundreds')

