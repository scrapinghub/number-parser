"""
The raw CLDR data was retreived on 25th Jun , 2020 from the following link
https://github.com/unicode-cldr/cldr-rbnf
"""

import os
import json
import re
from collections import OrderedDict

SUPPLEMENTARY_PATH = "../number_parser_data/supplementary_translation_data/"
f = ["UNIT_NUMBERS","DIRECT_NUMBERS","TENS","HUNDREDS","BIG_POWERS_OF_TEN"]
tokens = "SKIP_TOKENS"

for file_name in os.listdir(SUPPLEMENTARY_PATH):
    if file_name == "en.json":
        continue
    new_dic = {"NUMBERS": {} , "ORDINAL_NUMBERS": {}}
    full_supplementary_path = os.path.join(SUPPLEMENTARY_PATH, file_name)
    with open(full_supplementary_path, 'r') as source:
        data = json.load(source)
    for i in range(5):
        new_dic["NUMBERS"][f[i]] = data[f[i]]
        new_dic["ORDINAL_NUMBERS"][f[i]] = {}
    
    new_dic[tokens] = data[tokens]
    new_dic["IS_LONG"] = False
    # print(new_dic,file_name)
    # break
    mfinal = json.dumps(new_dic, indent=4, ensure_ascii=False)
    with open(full_supplementary_path, 'w') as ff:
        ff.write(mfinal)
    # break

# VALID_KEYS = ["spellout-cardinal", "spellout-numbering"]
# def _is_valid(key):
#     """Identifying whether the given key of the source language file needs to be extracted."""
#     is_valid = False
#     for valid_key in VALID_KEYS:
#         if valid_key in key:
#             is_valid = True
#     return is_valid

# def _count_zero(number):
#     """Counting the number of zeroes in the given number."""
#     zero_count = 0
#     while number > 9:
#         if number % 10 == 0:
#             zero_count += 1
#             number /= 10
#         else:
#             break
#     return zero_count


# fset = {}


# PATH_TO_FILE = "/home/arnav/GSOC_2020/number-parser/number_parser_data/raw_cldr_translation_data/"
# with open(PATH_TO_FILE + "ru.json") as f:
#     data = json.load(f)
#     requisite_data = data['rbnf']['rbnf']['SpelloutRules']
#     for keys, vals in requisite_data.items():
#         if _is_valid(keys):
#             for key, val in vals.items():
#                 try:
#                     if _count_zero((int)(key)) == 2:
#                         if key[0] == "1":
#                             continue
#                         get_vals = val.split("<")
#                         get_val = get_vals[1]
#                         suffix = get_vals[-1].split("[")[0]
#                         rq1 = get_val[1:]
#                         rq2  = rq1.replace("feminine", "masculine")
#                         rq3 = rq1.replace("masculine", "feminine")

#                         fd = (int)(key) // 100
#                         d1 = requisite_data["%" + rq1]
#                         d2 = requisite_data["%" + rq2]
#                         d3 = requisite_data["%" + rq3]
                        
#                         if(get_vals[-1] == "сти[ >>];"):
#                             for i in range(fd,3):
#                                 prefix = d3[str(i)]
#                                 prefix = prefix[:-1]
#                                 fset[prefix+suffix] = i*100
#                                 prefix = d2[str(i)]
#                                 prefix = prefix[:-1]
#                                 fset[prefix+suffix] = i*100
                                

#                         elif (get_vals[-1] == "ста[ >>];"):
#                             for i in range(fd,5):
#                                 prefix = d2[str(i)]
#                                 prefix = prefix[:-1]
#                                 fset[prefix+suffix] = i*100
#                                 # print(i*100,prefix+suffix)
#                         else:
#                             for i in range(fd,10):
#                                 prefix = d2[str(i)]
#                                 prefix = prefix[:-1]
#                                 fset[prefix+suffix] = i*100
#                                 # print(i*100,prefix+suffix)
#                             # print(d2)
#                 except:
#                     pass

# fdict = OrderedDict()
# mvals = (sorted(fset.items(), key=lambda x: x[1]))

# for each in mvals:
#     fdict[each[0]] = each[1]

# RT_PATH = "/home/arnav/GSOC_2020/number-parser/number_parser_data/supplementary_translation_data"
# mfinal = {}
# with open(RT_PATH + "/ru.json" ) as f:
#     data = json.load(f)
#     data["HUNDREDS"].update(fdict)
#     mfinal = json.dumps(data, indent=4, ensure_ascii=False)
# print(mfinal)
# with open(RT_PATH + "/ru.json","w" ) as ff:
#     ff.write(mfinal)


