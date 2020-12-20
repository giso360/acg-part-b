a_1 = [{"a": 5, "b": 2}]
real = [{"a": 5, "b": 2}]
pred = [{"a": 5}]
pred = [{"a": 4, "b": 0}]
a_2 = [{"a": 5, "b": 2}]


def _equalize_dictionaries_for_frequency(true_dict, approx_dict):
    print(true_dict)
    print(approx_dict)
    true_keys = list(true_dict.keys())
    approx_keys = list(approx_dict.keys())
    missing_keys_from_approx = list(set(true_keys) - set(approx_keys))
    for missing_key in missing_keys_from_approx:
        approx_dict[missing_key] = 0
    return approx_dict


def _equalize_dictionaries_for_rankings(true_dict, approx_dict):
    print(true_dict)
    print(approx_dict)
    true_keys = list(true_dict.keys())
    approx_keys = list(approx_dict.keys())
    counter = 0
    for true_key in true_keys:
        if true_key not in approx_keys:
            true_dict.pop(true_key)
            counter = counter + 1
    return true_dict, counter


def _evaluate_MAE_MAPE(true_dict, approximate_equalized_dict, missing_rankings=0):
    maei = 0
    mapei = 0
    counter = 0
    for entity_key in list(true_dict.keys()):
        true_value = true_dict[entity_key]
        approx_value = approximate_equalized_dict[entity_key]
        maei = maei + abs(true_value - approx_value)
        if true_value != 0:
            mapei = mapei + abs((true_value - approx_value) / true_value)
        counter = counter + 1
    if missing_rankings != 0:
        maei = maei + 1
        mapei = mapei + 1
        counter = counter + 1
    mae = round(maei / counter, 2)
    mape = round((mapei / counter) * 100, 2)
    return mae, mape


def evaluate_accuracy_on_frequency(true_list_dicts, approximate_list_dicts):
    true_dict = true_list_dicts[0]
    approx_dict = approximate_list_dicts[0]
    approx_dict = _equalize_dictionaries_for_frequency(true_dict, approx_dict)
    mae, mape = _evaluate_MAE_MAPE(true_dict, approx_dict)
    return mae, mape


def evaluate_accuracy_on_rankigs(true_list_dicts, approximate_list_dicts):
    true_dict = true_list_dicts[0]
    approx_dict = approximate_list_dicts[0]
    true_dict, missing_rankings = _equalize_dictionaries_for_rankings(true_dict, approx_dict)
    true_dict_keys = list(true_dict)
    approx_dict_keys = list(approx_dict)
    wrong_places = 0
    for i in range(0, len(true_dict_keys)):
        if true_dict_keys[i] != approx_dict_keys[i]:
            wrong_places = wrong_places + 1
    if len(true_dict_keys) == 0:
        wrong_places_percent = 0
    else:
        wrong_places_percent = (wrong_places / len(true_dict_keys)) * 100
    return wrong_places_percent, missing_rankings


print(evaluate_accuracy_on_frequency(a_1, a_2))
