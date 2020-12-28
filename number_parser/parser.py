import re
from importlib import import_module
import unicodedata
SENTENCE_SEPARATORS = [".", ","]
SUPPORTED_LANGUAGES = ['en', 'es', 'hi', 'ru']
RE_BUG_LANGUAGES = ['hi']


class LanguageData:
    """Main language class to populate the requisite language-specific variables."""
    unit_numbers = {}
    direct_numbers = {}
    tens = {}
    hundreds = {}
    big_powers_of_ten = {}
    skip_tokens = []
    all_numbers = {}
    unit_and_direct_numbers = {}

    def __init__(self, language):
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f'"{language}" is not a supported language')
        language_info = getattr(import_module('number_parser.data.' + language), 'info')
        self.unit_numbers = _normalize_dict(language_info["UNIT_NUMBERS"])
        self.direct_numbers = _normalize_dict(language_info["DIRECT_NUMBERS"])
        self.tens = _normalize_dict(language_info["TENS"])
        self.hundreds = _normalize_dict(language_info["HUNDREDS"])
        self.big_powers_of_ten = _normalize_dict(language_info["BIG_POWERS_OF_TEN"])
        self.skip_tokens = language_info["SKIP_TOKENS"]

        self.all_numbers = {**self.unit_numbers, **self.direct_numbers, **self.tens,
                            **self.hundreds, **self.big_powers_of_ten}
        self.unit_and_direct_numbers = {**self.unit_numbers, **self.direct_numbers}
        self.maximum_group_value = 10000 if language_info["USE_LONG_SCALE"] else 100


def _check_validity(current_token, previous_token, previous_power_of_10, total_value, current_grp_value, lang_data):
    """Identifies whether the new token can continue building the previous number."""
    if previous_token is None:
        return True

    if current_token in lang_data.unit_and_direct_numbers and previous_token in lang_data.unit_and_direct_numbers:
        # both tokens are "units" or "direct numbers"
        return False

    elif current_token in lang_data.direct_numbers and previous_token in lang_data.tens:
        # current token in "direct numbers" and previous token in "tens"
        return False

    elif current_token in lang_data.tens \
            and (previous_token in lang_data.tens or previous_token in lang_data.unit_and_direct_numbers):
        # current token in "tens" and previous token in "tens" or it's a "unit" or "direct number"
        return False

    elif current_token in lang_data.hundreds and previous_token not in lang_data.big_powers_of_ten:
        # current token in "hundreds" and previous token is not a "big power of ten"
        return False

    elif current_token in lang_data.big_powers_of_ten:
        # current token is a "big power of ten"
        power_of_ten = lang_data.big_powers_of_ten[current_token]
        if power_of_ten < current_grp_value:
            return False
        if total_value != 0 and previous_power_of_10 and power_of_ten >= previous_power_of_10:
            return False
    return True


def _check_large_multiplier(current_token, total_value, current_grp_value, lang_data):
    """Checks if the current token (power of ten) is larger than the total value formed till now."""
    combined_value = total_value + current_grp_value
    if combined_value and current_token in lang_data.big_powers_of_ten:
        large_value = lang_data.big_powers_of_ten[current_token]
        if large_value > combined_value and large_value != 100:
            return True
    return False


def _build_number(token_list, lang_data):
    """Incrementaly builds a number from the list of tokens."""
    total_value = 0
    current_grp_value = 0
    previous_token = None
    previous_power_of_10 = None
    value_list = []
    used_skip_tokens = []

    for token in token_list:
        if not token.strip():
            continue
        if token in lang_data.skip_tokens:
            used_skip_tokens.append(token)
            continue

        is_large_multiplier = _check_large_multiplier(token, total_value, current_grp_value, lang_data)
        if is_large_multiplier:
            combined_value = total_value + current_grp_value
            total_value = combined_value * lang_data.big_powers_of_ten[token]
            previous_token = token
            current_grp_value = 0
            used_skip_tokens = []
            previous_power_of_10 = lang_data.big_powers_of_ten[token]
            continue

        valid = _check_validity(token, previous_token, previous_power_of_10, total_value, current_grp_value, lang_data)
        if not valid:
            total_value += current_grp_value
            value_list.append(str(total_value))
            total_value = 0
            current_grp_value = 0
            for skip_token in used_skip_tokens:
                value_list.append(skip_token)
            previous_power_of_10 = None

        if token in lang_data.unit_and_direct_numbers:
            current_grp_value += lang_data.unit_and_direct_numbers[token]

        elif token in lang_data.tens:
            current_grp_value += lang_data.tens[token]

        elif token in lang_data.hundreds:
            current_grp_value += lang_data.hundreds[token]

        elif token in lang_data.big_powers_of_ten:
            power_of_ten = lang_data.big_powers_of_ten[token]
            if current_grp_value == 0:
                current_grp_value = 1

            current_grp_value *= power_of_ten
            if power_of_ten > lang_data.maximum_group_value:
                total_value += current_grp_value
                current_grp_value = 0
                previous_power_of_10 = power_of_ten

        previous_token = token
        used_skip_tokens = []
    total_value += current_grp_value
    value_list.append(str(total_value))
    return value_list


def _tokenize(input_string, language):
    """Breaks string on any non-word character."""
    input_string = input_string.replace('\xad', '')
    if language in RE_BUG_LANGUAGES:
        return re.split(r'(\s+)', input_string)
    return re.split(r'(\W)', input_string)


def _strip_accents(word):
    """Removes accent from the input word."""
    return ''.join(char for char in unicodedata.normalize('NFD', word) if unicodedata.category(char) != 'Mn')


def _normalize_tokens(token_list):
    """Converts all tokens to lowercase then removes accents."""
    return [_strip_accents(token.lower()) for token in token_list]


def _normalize_dict(lang_data):
    """Removes the accent from each key of input dictionary"""
    return {_strip_accents(word): number for word, number in lang_data.items()}


def _is_cardinal_token(token, lang_data):
    """Checks if the given token is a cardinal number and returns token"""
    if token in lang_data.all_numbers:
        return token
    return None


def _is_ordinal_token(token, lang_data):
    """Checks if the given token is a ordinal number and returns token"""
    if _is_cardinal_token(token, lang_data) is None:
        return _is_number_token(token, lang_data)
    return None


def _is_number_token(token, lang_data):
    """
    Checks if the given token belongs to either cardinal or ordinal numbers
    and returns the cardinal form.
    """
    token = _apply_cardinal_conversion(token, lang_data)
    return _is_cardinal_token(token, lang_data)


def _is_skip_token(token, lang_data):
    return token in lang_data.skip_tokens


def _apply_cardinal_conversion(token, lang_data):  # Currently only for English language.
    """Converts ordinal tokens to cardinal while leaving other tokens unchanged."""
    CARDINAL_DIRECT_NUMBERS = {'first': 'one', 'second': 'two', 'third': 'three', 'fifth': 'five', 'eighth': 'eight',
                               'ninth': 'nine', 'twelfth': 'twelve'}

    for word, number in CARDINAL_DIRECT_NUMBERS.items():
        token = token.replace(word, number)

    token_cardinal_form_1 = re.sub(r'ieth$', 'y', token)
    if _is_cardinal_token(token_cardinal_form_1, lang_data) is not None:
        return token_cardinal_form_1

    token_cardinal_form_2 = re.sub(r'th$', '', token)
    if _is_cardinal_token(token_cardinal_form_2, lang_data) is not None:
        return token_cardinal_form_2

    return token


def _valid_tokens_by_language(input_string):
    language_matches = {}

    for language in SUPPORTED_LANGUAGES:
        lang_data = LanguageData(language)
        tokens = _tokenize(input_string, language)
        normalized_tokens = _normalize_tokens(tokens)
        valid_list = [
            _is_number_token(token, lang_data) is not None or _is_skip_token(token, lang_data)
            for token in normalized_tokens
        ]
        cnt_valid_words = valid_list.count(True)
        language_matches[language] = cnt_valid_words

    best_language = max(language_matches, key=language_matches.get)
    if language_matches[best_language] == 0:  # return English if not matching words
        return 'en'
    return best_language


def parse_ordinal(input_string, language=None):
    """Converts a single number in ordinal or cardinal form to it's numeric equivalent"""
    if language is None:
        language = _valid_tokens_by_language(input_string)

    lang_data = LanguageData(language)
    tokens = _tokenize(input_string, language)
    normalized_tokens = _normalize_tokens(tokens)
    processed_tokens = [_apply_cardinal_conversion(token, lang_data) for token in normalized_tokens]
    output_string = ' '.join(processed_tokens)
    return parse_number(output_string, language)


def parse_number(input_string, language=None):
    """Converts a single number written in natural language to a numeric type"""
    if not input_string.strip():
        return None

    if input_string.strip().isnumeric():
        return int(input_string)

    if language is None:
        language = _valid_tokens_by_language(input_string)

    lang_data = LanguageData(language)

    tokens = _tokenize(input_string, language)
    normalized_tokens = _normalize_tokens(tokens)
    for index, token in enumerate(normalized_tokens):
        if _is_cardinal_token(token, lang_data) or not token.strip():
            continue
        if _is_skip_token(token, lang_data) and index != 0:
            continue
        return None
    number_built = _build_number(normalized_tokens, lang_data)
    if len(number_built) == 1:
        return int(number_built[0])
    return None


def parse(input_string, language=None):
    """
    Converts all the numbers in a sentence written in natural language to their numeric type while keeping
    the other words unchanged. Returns the transformed string.
    """
    if language is None:
        language = _valid_tokens_by_language(input_string)

    lang_data = LanguageData(language)

    tokens = _tokenize(input_string, language)

    final_sentence = []
    current_sentence = []
    tokens_taken = []

    def _build_and_add_number(pop_last_space=False):
        if tokens_taken:
            result = _build_number(tokens_taken, lang_data)
            tokens_taken.clear()

            for number in result:
                current_sentence.extend([number, " "])

            if pop_last_space:
                current_sentence.pop()

    for token in tokens:
        compare_token = _strip_accents(token.lower())
        ordinal_number = _is_ordinal_token(compare_token, lang_data)

        if not compare_token.strip():
            if not tokens_taken:
                current_sentence.append(token)
            continue

        if compare_token in SENTENCE_SEPARATORS:
            _build_and_add_number(pop_last_space=True)
            current_sentence.append(token)
            final_sentence.extend(current_sentence)
            current_sentence = []
            continue

        if ordinal_number:
            tokens_taken.append(ordinal_number)
            _build_and_add_number(pop_last_space=True)
        elif (
                _is_cardinal_token(compare_token, lang_data)
                or (_is_skip_token(compare_token, lang_data) and len(tokens_taken) != 0)
        ):
            tokens_taken.append(compare_token)
        else:
            if tokens_taken and _is_skip_token(tokens_taken[-1], lang_data):
                # when finishing with a skip_token --> keep it
                skip_token = tokens_taken[-1]
                tokens_taken.pop()
                _build_and_add_number()
                current_sentence.extend([skip_token, " "])

            _build_and_add_number()
            current_sentence.append(token)

    _build_and_add_number()

    final_sentence.extend(current_sentence)
    return ''.join(final_sentence).strip()
