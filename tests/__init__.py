import csv
from pathlib import Path

from number_parser import parse_number, parse_ordinal

TEST_ROOT = Path(__file__).resolve().parent
HUNDREDS_DIRECTORY = TEST_ROOT / "data" / "hundreds"
PERMUTATION_DIRECTORY = TEST_ROOT / "data" / "permutations"
ORDINALS_DIRECTORY = TEST_ROOT / "data" / "ordinals"
ORDINALS_PERMUTATION_DIRECTORY = TEST_ROOT / "data" / "ordinals_permutations"


def get_test_files(path, prefix):
    return [file for file in Path(path).iterdir() if file.name.startswith(prefix)]


def _test_files(path, language, is_ordinal=True):
    fnx = parse_ordinal if is_ordinal else parse_number
    for filename in get_test_files(path, f"{language}_"):
        with filename.open(encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                try:
                    assert fnx(row["text"], language) == int(row["number"])
                except AssertionError as e:
                    raise AssertionError(
                        f'Failed execution of {row["text"]} (file: "{filename}")'
                    ) from e
