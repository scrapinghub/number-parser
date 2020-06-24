import json
from git import Repo

def get_raw_data():
    cldr_rbnf_url = "https://github.com/unicode-cldr/cldr-rbnf.git"
    numeral_data_directory = "../number_parser/numeral_translation_data"
    Repo.clone_from(cldr_rbnf_url, numeral_data_directory , branch='master')

get_raw_data()