import json
from probables.hashes import (default_sha256)
from probables import (CountMinSketch)
from probables import (HeavyHitters)


def sort_dict_by_value_desc(dictionary):
    dictionary_sorted_keys = sorted(dictionary, key=dictionary.get, reverse=True)
    res = {}
    for r in dictionary_sorted_keys:
        res[r] = dictionary[r]
    return res


cms = CountMinSketch(width=2000, depth=10, hash_function=default_sha256)
hh = HeavyHitters(num_hitters=10, width=2000, depth=10, hash_function=default_sha256)
with open("./data/tweets.json.3", encoding='cp850') as fl:
    for line in fl:
        c = json.loads(line)
        username = c["user"]["screen_name"]
        cms.add(username)
        hh.add(username)

users_to_check = ["QbanKendy", "Farhansyah_15", "KhanOli"]

for user in users_to_check:
    print(cms.check(user))

print("------------")
print(sort_dict_by_value_desc(hh.heavy_hitters))