import json
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

months_dict = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}


def created_at_to_datetime(created_at):
    created_at = created_at.split(sep=" ")
    created_at = months_dict[created_at[1]] + "/" + created_at[2] + "/" + created_at[-1] + " " + created_at[3]
    created_at = datetime.strptime(created_at, '%m/%d/%Y %H:%M:%S')
    return created_at


def entity_count_dictionary(entity_list):
    return dict([(i, entity_list.count(i)) for i in set(entity_list)])


def sort_dict_by_value_desc(dictionary):
    dictionary_sorted_keys = sorted(dictionary, key=dictionary.get, reverse=True)
    res = {}
    for r in dictionary_sorted_keys:
        res[r] = dictionary[r]
    return res


# file = open("data/testjsons/tiny.json.1000", 'r', encoding='cp850')
file = open("data/testjsons/tweets.json.13", 'r', encoding='cp850')
# file = open("./data/tweets.json.3", 'r', encoding='cp850')

lines = file.readlines()
tweets = []
users = []
hashtags = []
tweet_times = []
tweet_ids = []

for line in lines:
    c = json.loads(line)
    hstgs = []
    tweets.append(json.loads(line))
    username = c["user"]["screen_name"]
    users.append(username)
    for tag in c["entities"]["hashtags"]:
        hstgs.append(tag.get("text"))
    hashtags.append(hstgs)
    tweet_times.append(created_at_to_datetime(c.get("user").get("created_at")))
    tweet_ids.append(c.get("id"))


# print(tweet_times)
# print(sorted(tweet_times))
# print(sorted(tweet_times)[-1] - sorted(tweet_times)[0])
# print(tweet_ids)
# print(tweet_times)


users_dict = entity_count_dictionary(users)
users_dict_sorted = sort_dict_by_value_desc(users_dict)
print("The memory used by the object storing user counts is: ", sys.getsizeof(users_dict_sorted), " bytes.")
with open('out/tweet_users.csv', 'w') as f:
    for key in users_dict_sorted.keys():
        f.write("%s,%s\n" % (key, users_dict_sorted[key]))

hashtags = [h for sublist in hashtags for h in sublist]
hashtag_dict = entity_count_dictionary(hashtags)
hashtag_dict_sorted = sort_dict_by_value_desc(hashtag_dict)
print("The memory used by the object storing hashtag counts is: ", sys.getsizeof(hashtag_dict_sorted), " bytes.")
with open('out/tweet_hashtags.csv', 'w', encoding='cp850') as f:
    for key in hashtag_dict_sorted.keys():
        f.write("%s,%s\n" % (key, hashtag_dict_sorted[key]))


data = []
for i in range(0, len(tweet_ids)):
    pair = [tweet_ids[i], tweet_times[i]]
    data.append(pair)

print(data)
df = pd.DataFrame(data=data, columns=["id", "time"])
df["time"] = df["time"].apply(lambda time: time.date())
print(df.head())
min_date = df["time"].min()
print(df["time"].min())
max_date = df["time"].max()
print(df["time"].max())
# x = df["time"]
df.groupby(["time"]).size().plot.bar()
# plt.xticks([datetime.strftime(min_date, '%m/%d/%Y'), datetime.strftime(max_date, '%m/%d/%Y')])
# plt.show()


# How many unique users are there? Deterministic approach; check against HyperLog
no_of_unique_users = set(users)
print("Number of unique users is: ", len(no_of_unique_users))
# How many unique tags are there? Deterministic approach; check against HyperLog
no_of_unique_hashtags = set(hashtags)
print("Number of unique hashtags is: ", len(no_of_unique_hashtags))



##############################
