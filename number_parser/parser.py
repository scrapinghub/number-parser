import re
import unicodedata
from importlib import import_module

SENTENCE_SEPARATORS = [".", ","]
SUPPORTED_LANGUAGES = [
    "en",
    "es",
    "hi",
    "ru",
    "uk",
    "ja",
    "ko",
    "zh",
    "zh-Hant",
    "yue",
    "yue-Hans",
]
RE_BUG_LANGUAGES = ["hi"]
_CJK_LANGUAGES = ["ja", "ko", "zh", "zh-Hant", "yue", "yue-Hans"]
_CJK_MYRIAD = 10_000
_CJK_ORDINAL_RE = re.compile(r"(?:第|제)?(.*?)(?:番目)?")


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
        language_info = getattr(import_module("number_parser.data." + language), "info")
        self.unit_numbers = _normalize_dict(language_info["UNIT_NUMBERS"])
        self.direct_numbers = _normalize_dict(language_info["DIRECT_NUMBERS"])
        self.tens = _normalize_dict(language_info["TENS"])
        self.hundreds = _normalize_dict(language_info["HUNDREDS"])
        self.big_powers_of_ten = _normalize_dict(language_info["BIG_POWERS_OF_TEN"])
        self.skip_tokens = language_info["SKIP_TOKENS"]

        self.all_numbers = {
            **self.unit_numbers,
            **self.direct_numbers,
            **self.tens,
            **self.hundreds,
            **self.big_powers_of_ten,
        }
        self.unit_and_direct_numbers = {**self.unit_numbers, **self.direct_numbers}
        self.maximum_group_value = 10000 if language_info["USE_LONG_SCALE"] else 100
        self._is_cjk = language in _CJK_LANGUAGES
        self._is_ko = language == "ko"


def _check_validity(
    current_token,
    previous_token,
    previous_power_of_10,
    total_value,
    current_grp_value,
    lang_data,
):
    """Identifies whether the new token can continue building the previous number."""
    if previous_token is None:
        return True

    if (
        current_token in lang_data.unit_and_direct_numbers
        and previous_token in lang_data.unit_and_direct_numbers
    ):
        # both tokens are "units" or "direct numbers"
        return False

    elif current_token in lang_data.direct_numbers and previous_token in lang_data.tens:
        # current token in "direct numbers" and previous token in "tens"
        return False

    elif current_token in lang_data.tens and (
        previous_token in lang_data.tens
        or previous_token in lang_data.unit_and_direct_numbers
    ):
        # current token in "tens" and previous token in "tens" or it's a "unit" or "direct number"
        return False

    elif (
        current_token in lang_data.hundreds
        and previous_token not in lang_data.big_powers_of_ten
    ):
        # current token in "hundreds" and previous token is not a "big power of ten"
        return False

    elif current_token in lang_data.big_powers_of_ten:
        # current token is a "big power of ten"
        power_of_ten = lang_data.big_powers_of_ten[current_token]
        if power_of_ten < current_grp_value:
            return False
        if (
            total_value != 0
            and previous_power_of_10
            and power_of_ten >= previous_power_of_10
        ):
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


def _build_cjk_number(token_list, lang_data):
    """
    Builds numbers from CJK tokens, where 十, 百 and 千 multiply the digit
    before them, and 万, 億 and bigger multiply everything before them since
    the previous bigger multiplier. Digits without multipliers, e.g. 二〇二四,
    are read positionally, except in Korean.
    """
    value_list = []
    total = section = 0
    digit = None
    digits = ""
    last_small = last_big = None

    def _value():
        if digits:
            return int(digits)
        return total + section + (digit or 0)

    for token in token_list:
        if not token.strip():
            continue
        is_multiplier = token in lang_data.big_powers_of_ten
        in_positional_run = len(digits) > 1
        if is_multiplier:
            multiplier = lang_data.big_powers_of_ten[token]
            below = section + (digit or 0)
            if multiplier < _CJK_MYRIAD:
                valid = not in_positional_run and (
                    last_small is None or multiplier < last_small
                )
            else:
                valid = not in_positional_run and (
                    last_big is None
                    or multiplier < last_big
                    or total + below < multiplier
                )
        else:
            valid = (
                digit is None
                or (digits and not total and not section and not lang_data._is_ko)
                or (digit == 0 and (total or section))
            )
        if not valid:
            value_list.append(str(_value()))
            total = section = 0
            digit = None
            digits = ""
            last_small = last_big = None

        if not is_multiplier:
            digit = lang_data.unit_numbers[token]
            if not total and not section:
                digits += str(digit)
            continue
        digits = ""
        if multiplier < _CJK_MYRIAD:
            section += (1 if digit is None else digit) * multiplier
            last_small = multiplier
        else:
            below = section + (digit or 0)
            if last_big is not None and multiplier > last_big:
                total = (total + below) * multiplier
            else:
                total += (below or 1) * multiplier
            section = 0
            last_small = None
            last_big = multiplier
        digit = None

    value_list.append(str(_value()))
    return value_list


def _build_number(token_list, lang_data):
    """Incrementally builds a number from the list of tokens."""
    if lang_data._is_cjk:
        return _build_cjk_number(token_list, lang_data)
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

        is_large_multiplier = _check_large_multiplier(
            token, total_value, current_grp_value, lang_data
        )
        if is_large_multiplier:
            combined_value = total_value + current_grp_value
            total_value = combined_value * lang_data.big_powers_of_ten[token]
            previous_token = token
            current_grp_value = 0
            used_skip_tokens = []
            previous_power_of_10 = lang_data.big_powers_of_ten[token]
            continue

        valid = _check_validity(
            token,
            previous_token,
            previous_power_of_10,
            total_value,
            current_grp_value,
            lang_data,
        )
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
    input_string = input_string.replace("\xad", "")
    if language in RE_BUG_LANGUAGES:
        return re.split(r"(\s+)", input_string)
    if language in _CJK_LANGUAGES:
        return list(input_string)
    return re.split(r"(\W)", input_string)


def _strip_accents(word):
    """Removes accent from the input word."""
    return "".join(
        char
        for char in unicodedata.normalize("NFD", word)
        if unicodedata.category(char) != "Mn"
    )


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


def _apply_cardinal_conversion(
    token, lang_data
):  # Currently only for English language.
    """Converts ordinal tokens to cardinal while leaving other tokens unchanged."""
    CARDINAL_DIRECT_NUMBERS = {
        "first": "one",
        "second": "two",
        "third": "three",
        "fifth": "five",
        "eighth": "eight",
        "ninth": "nine",
        "twelfth": "twelve",
    }

    for word, number in CARDINAL_DIRECT_NUMBERS.items():
        token = token.replace(word, number)

    token_cardinal_form_1 = re.sub(r"ieth$", "y", token)
    if _is_cardinal_token(token_cardinal_form_1, lang_data) is not None:
        return token_cardinal_form_1

    token_cardinal_form_2 = re.sub(r"th$", "", token)
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
            _is_number_token(token, lang_data) is not None
            or _is_skip_token(token, lang_data)
            for token in normalized_tokens
        ]
        cnt_valid_words = valid_list.count(True)
        language_matches[language] = cnt_valid_words

    best_language = max(language_matches, key=language_matches.get)
    if language_matches[best_language] == 0:  # return English if not matching words
        return "en"
    return best_language


def parse_ordinal(input_string, language=None):
    """Converts a single number in ordinal or cardinal form to it's numeric equivalent"""
    if language is None:
        language = _valid_tokens_by_language(input_string)

    if language in _CJK_LANGUAGES:
        number = _CJK_ORDINAL_RE.fullmatch(input_string.strip())[1]
        return parse_number(number, language)

    lang_data = LanguageData(language)
    tokens = _tokenize(input_string, language)
    normalized_tokens = _normalize_tokens(tokens)
    processed_tokens = [
        _apply_cardinal_conversion(token, lang_data) for token in normalized_tokens
    ]
    output_string = " ".join(processed_tokens)
    return parse_number(output_string, language)


def parse_number(input_string, language=None):
    """Converts a single number written in natural language to a numeric type"""
    if not input_string.strip():
        return None

    if input_string.strip().isdecimal():
        return int(input_string)

    if language is None:
        language = _valid_tokens_by_language(input_string)

    lang_data = LanguageData(language)

    # Normalize the input string by removing apostrophes
    input_string = input_string.replace("'", "")
    input_string = input_string.replace("’", "")

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


def parse_fraction(input_string, language=None):
    """Converts a single number written in fraction to a numeric type"""
    if not input_string.strip():
        return None

    if language is None:
        language = _valid_tokens_by_language(input_string)

    FRACTION_SEPARATORS = ["divided by", "over", "by", "/"]

    for separator in FRACTION_SEPARATORS:
        position_of_separator = input_string.find(separator)

        if position_of_separator == -1:
            continue

        string_before_separator = input_string[:position_of_separator]
        string_after_separator = input_string[position_of_separator + len(separator) :]

        number_before_separator = parse_number(string_before_separator, language)
        number_after_separator = parse_number(string_after_separator, language)

        if number_before_separator is None or number_after_separator is None:
            return None

        return f"{number_before_separator}/{number_after_separator}"

    return None


def _parse_korean(input_string, lang_data):
    """
    Korean number syllables are also common words and particles, e.g. 이 (this)
    or 만 (only), so only runs of 2+ syllables at the start of a word count.
    Trailing syllables that would start another number are left as text, e.g.
    일 (day) in 이십오일.
    """
    # ponytail: words made only of number syllables, e.g. 구조 (structure),
    # still get converted; a word list would be needed to tell them apart.
    chars = "".join(
        unicodedata.normalize("NFC", token) for token in lang_data.all_numbers
    )
    group = r"(?<!\w)[" + chars + "]{2,}"
    pattern = group + r"(?:(?<=[만억조])\s+" + group + ")*"

    def _replace(match):
        text = match.group()
        while True:
            numbers = _build_cjk_number(_normalize_tokens(list(text)), lang_data)
            if len(numbers) == 1:
                break
            text = text[:-1].rstrip()
        if len(text) < 2:
            return match.group()
        return numbers[0] + match.group()[len(text) :]

    return re.sub(pattern, _replace, input_string)


def parse(input_string, language=None):
    """
    Converts all the numbers in a sentence written in natural language to their numeric type while keeping
    the other words unchanged. Returns the transformed string.
    """
    if language is None:
        language = _valid_tokens_by_language(input_string)

    lang_data = LanguageData(language)
    if lang_data._is_ko:
        return _parse_korean(input_string, lang_data)

    tokens = _tokenize(input_string, language)

    final_sentence = []
    current_sentence = []
    tokens_taken = []
    pop_last_space = True

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
                pop_last_space = True
            else:
                pop_last_space = False
            continue

        if compare_token in SENTENCE_SEPARATORS:
            _build_and_add_number(pop_last_space=pop_last_space)
            current_sentence.append(token)
            final_sentence.extend(current_sentence)
            current_sentence = []
            continue

        if ordinal_number:
            tokens_taken.append(ordinal_number)
            _build_and_add_number(pop_last_space=True)
        elif _is_cardinal_token(compare_token, lang_data) or (
            _is_skip_token(compare_token, lang_data) and len(tokens_taken) != 0
        ):
            tokens_taken.append(compare_token)
        else:
            if tokens_taken and _is_skip_token(tokens_taken[-1], lang_data):
                # when finishing with a skip_token --> keep it
                skip_token = tokens_taken[-1]
                tokens_taken.pop()
                _build_and_add_number()
                current_sentence.extend([skip_token, " "])

            _build_and_add_number(pop_last_space=pop_last_space)
            current_sentence.append(token)

        pop_last_space = True

    _build_and_add_number()

    final_sentence.extend(current_sentence)
    return "".join(final_sentence).strip()
