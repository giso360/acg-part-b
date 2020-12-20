from probables import CountMinSketch
from probables.hashes import default_sha256

from util.fileutil import *
from util.util import flatten_list_of_lists, entity_frequencies_per_batch, sliding_cumulative_array, \
    merge_dictionaries_in_list, entity_count_dictionary, sort_dict_by_value_desc
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from util.evaluation_util import evaluate_accuracy_on_frequency, evaluate_accuracy_on_rankigs

sys.path.append("./data")

# *********************************************************************
# **********************1. ACCURATE SOLUTION***************************
# *********************************************************************

# #####################################################################
# #####################SCREEN_NAMES####################################
# #####################################################################

before = datetime.now()
# users_per_file_per_batch: [      [[batch1],[batch2]],     [[batch1],[batch2]]   ]
# Note the cumulative form: [[batch1],[batch1 + batch2]],     [all_batches]]]
users_per_file_per_batch = process_directory("./data/testjsons", get_screen_name_callback)
after = datetime.now()
print("\nGathering entities - Calculation took: ", (after - before).seconds, " seconds")

# users_per_batch: [[batch1],[batch2], [batch3], [batch4]]
users_per_batch = flatten_list_of_lists(users_per_file_per_batch)
# users_per_batch_frequency: [[{freq_dictionary}], ....]
users_per_batch_frequency = entity_frequencies_per_batch(users_per_batch)
# users = [user1, user2, user3, .....]
users = [e for e in flatten_list_of_lists(users_per_batch)]
users_set = set(users)

# #####################################################################
# users_per_batch_frequency_cumulative:
users_per_batch_frequency_cumulative = sliding_cumulative_array(users_per_batch_frequency)
# users_per_batch_frequency_cumulative_final: [[batch1],[batch1 + batch2]],     [all_batches]]] => in freq counts dicts
users_per_batch_frequency_cumulative_final = [merge_dictionaries_in_list(e)
                                              for e in users_per_batch_frequency_cumulative]
# a dictionary of frequencies for all users
users_frequencies_final = entity_count_dictionary(users)
# sort above by value
users_frequencies_final_sorted = sort_dict_by_value_desc(users_frequencies_final)
print("The memory used by the object storing USER counts is: ",
      sys.getsizeof(users_frequencies_final_sorted), " bytes.")

# #####################################################################
# #####################HASHTAGS########################################
# #####################################################################

before = datetime.now()
hashtags_per_file_per_batch = process_directory("./data/testjsons", get_hashtags_callback)
after = datetime.now()
print("\nGathering entities - Calculation took: ", (after - before).seconds, " seconds")

hashtags_per_batch = flatten_list_of_lists(hashtags_per_file_per_batch)
hashtags_per_batch_frequency = entity_frequencies_per_batch(hashtags_per_batch)
hashtags = [e for e in flatten_list_of_lists(hashtags_per_batch)]
hashtags_set = set(hashtags)
# #####################################################################

hashtags_per_batch_frequency_cumulative = sliding_cumulative_array(hashtags_per_batch_frequency)

hashtags_per_batch_frequency_cumulative_final = [merge_dictionaries_in_list(e)
                                                 for e in hashtags_per_batch_frequency_cumulative]

hashtags_frequencies_final = entity_count_dictionary(hashtags)
hashtags_frequencies_final_sorted = sort_dict_by_value_desc(hashtags_frequencies_final)
print("The memory used by the object storing HASHTAG counts is: ",
      sys.getsizeof(hashtags_frequencies_final_sorted), " bytes.")

# #####################################################################
# #####################SAVE RESULTS TO CSV FILE########################
# #####################################################################

with open('out/tweet_users.csv', 'w') as f:
    for key in users_frequencies_final_sorted.keys():
        f.write("%s,%s\n" % (key, users_frequencies_final_sorted[key]))

with open('out/tweet_hashtags.csv', 'w', encoding = 'utf8') as f:
    for key in hashtags_frequencies_final_sorted.keys():
        f.write("%s,%s\n" % (key, hashtags_frequencies_final_sorted[key]))

# #####################################################################
# #####################VISUALIZATIONS##################################
# #####################################################################

# TOP 3
top = 3
# USERS
fig = plt.figure()
users_for_plot = list(users_frequencies_final_sorted.keys())[:top+1]
counts = list(users_frequencies_final_sorted.values())[:top+1]
plt.bar(users_for_plot, counts, color='blue')
plt.xticks(rotation=90)
plt.xlabel("screen_names", fontsize=15)
plt.ylabel("screen_names counts", fontsize=15)
plt.show()

# HASHTAGS
fig = plt.figure()
hashtags_for_plot = list(hashtags_frequencies_final_sorted.keys())[:top+1]
counts = list(hashtags_frequencies_final_sorted.values())[:top+1]
plt.bar(hashtags_for_plot, counts, color='blue')
plt.xticks(rotation=90)
plt.xlabel("hashtagss", fontsize=15)
plt.ylabel("hashtags counts", fontsize=15)
plt.show()


# *********************************************************************
# **********************2. APPROXIMATE SOLUTION************************
# *********************************************************************

# #####################################################################
# #####################SCREEN_NAMES####################################
# #####################################################################

# 1. CMS
print("====================")
print("=========CMS===========")
cms_per_batch =[]

total_width = 2400
total_depth = 12

cms = CountMinSketch(width=total_width, depth=total_depth, hash_function=default_sha256)
print("user results:")
print("user results:")
print("user results:")
for user in users:
    cms.add(user)



cms_user_freq = {}
for user in users:
    cms_user_freq[user] = cms.check(user)
print(cms_user_freq)
print("CMS - error for USER frequency: ", evaluate_accuracy_on_frequency([users_frequencies_final_sorted], [cms_user_freq]))
print("CMS - error for USER ranking: ", evaluate_accuracy_on_rankigs([users_frequencies_final_sorted], [cms_user_freq]))

cms = CountMinSketch(width=total_width, depth=total_depth, hash_function=default_sha256)
print("hashtags results:")
print("hashtags results:")
print("hashtags results:")
for hashtag in hashtags:
    cms.add(hashtag)

cms_hashtag_freq = {}
for hashtag in hashtags:
    cms_hashtag_freq[hashtag] = cms.check(hashtag)
print("CMS - error for HASHTAG frequency: ", evaluate_accuracy_on_frequency([hashtags_frequencies_final_sorted], [cms_hashtag_freq]))
print("CMS - error for HASHTAG ranking: ", evaluate_accuracy_on_rankigs([hashtags_frequencies_final_sorted], [cms_hashtag_freq]))

# 2. HH
print("====================")
print("=========HHITTERS===========")

hh = HeavyHitters(num_hitters=10, width=total_width, depth=total_depth, hash_function=default_sha256)
for user in users:
    hh.add(user)

print("heavy_hitters for USERS are (TOP-10): ", hh.heavy_hitters)
print("HEAVY HITTERS for USERS - error for frequency: ", evaluate_accuracy_on_frequency([users_frequencies_final_sorted], [hh.heavy_hitters]))
print("HEAVY HITTERS for USERS - error for ranking: ", evaluate_accuracy_on_rankigs([users_frequencies_final_sorted], [hh.heavy_hitters]))

hh = HeavyHitters(num_hitters=10, width=total_width, depth=total_depth, hash_function=default_sha256)
for hashtag in hashtags:
    hh.add(hashtag)

print("heavy_hitters for HASHTAGS are (TOP-10): ", hh.heavy_hitters)
print("HEAVY HITTERS for HASHTAGS - error for frequency: ", evaluate_accuracy_on_frequency([hashtags_frequencies_final_sorted], [hh.heavy_hitters]))
print("HEAVY HITTERS for HASHTAGS - error for ranking: ", evaluate_accuracy_on_rankigs([users_frequencies_final_sorted], [hh.heavy_hitters]))

# 3. HYPERLOGOG
print("====================")
print("=========HYPERLOGLOG===========")

hll = HyperLogLog()

for user in users:
    hll.update(str(user).encode('utf8'))

print("HYPEROGLOG ERROR FOR USERS", hll.count() - len(users_set))

hll = HyperLogLog()

for hashtag in hashtags:
    hll.update(str(hashtag).encode('utf8'))

print("HYPEROGLOG ERROR FOR HASHTAGS", hll.count() - len(hashtags_set))






# # #####################################################################