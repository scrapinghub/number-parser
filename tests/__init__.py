import os
TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
HUNDREDS_DIRECTORY = os.path.join(TEST_ROOT, "./data/hundreds")
PERMUTATION_DIRECTORY = os.path.join(TEST_ROOT, "./data/permutations")


def get_test_files(path, prefix):
    return [
        os.path.join(path, filename)
        for filename in os.listdir(path)
        if filename.startswith(prefix)
    ]
