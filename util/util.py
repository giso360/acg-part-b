def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def sort_dict_by_value_desc(dictionary):
    dictionary_sorted_keys = sorted(dictionary, key=dictionary.get, reverse=True)
    res = {}
    for r in dictionary_sorted_keys:
        res[r] = dictionary[r]
    return res


def entity_count_dictionary(entity_list):
    """
    try: entity_count_dictionary(["a","a","b","b","b","c"])
    :param entity_list:
    :return: dictionary of frequencies for each element
    """
    result = dict([(i, entity_list.count(i)) for i in set(entity_list)])
    return result


def entity_frequencies_per_batch(entities_per_batch):
    """
    try: entity_frequencies_per_batch([["a","a","b","b","b","c"], ["a","b","b","c"]])
    :param entities_per_batch:
    :return: list of dictionaries for each batch
    """
    result = []
    for batch in entities_per_batch:
        result.append(entity_count_dictionary(batch))
    for freq_batch in result:
        freq_batch = sort_dict_by_value_desc(freq_batch)
    return result


def mergeDict(dict1, dict2):
    """
    try mergeDict({"a":1,"b":2},{"a":1,"b":4,"c":2})
   Source: https://thispointer.com/how-to-merge-two-or-more-dictionaries-in-python/
   Added check for type of value in dictionary.
   :param dict1:
   :param dict2:
   :return: a merged dictionary of 2 dicts
   """
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]
    for k, v in dict3.items():
        if type(v) == list:
            dict3[k] = sum(v)
    return dict3


def merge_dictionaries_in_list(list_of_dicts):
    """
    try: merge_dictionaries_in_list([{"a":1,"b":2},{"a":1,"b":4,"c":2}, {"a":1,"b":2}])
    :param list_of_dicts:
    :return: resultant dictionary
    """
    result = []
    for i in range(0, len(list_of_dicts)):
        if i == 0:
            result.append(list_of_dicts[i])
        else:
            res = mergeDict(result[0], list_of_dicts[i])
            result = [res]
    return result


def cumulative_freq_count(list_of_entities_per_batch_frequency):
    """
    :type list_of_entities_per_batch: list of dictionaries.
    use: users_per_batch_frequency
    """
    cumulative_entity_frequencies = sliding_cumulative_array(list_of_entities_per_batch_frequency)
    result = {}


def sliding_cumulative_array(array_in):
    """
    [1,2,3] -> [[1],[1,2],[1,2,3]]
    :param array_in:
    :return: cumulative array of arrays
    """
    result = []
    for i in range(0, len(array_in)):
        if i == 0:
            result.append([array_in[i]])
        else:
            k = []
            for j in range(0, i + 1):
                k.append(array_in[j])
            result.append(k)
    return result








print(sliding_cumulative_array([1,2,3]))
