def check_dict_case(dict):
    all_lower = True
    all_upper = True
    seen_key = False
    key = None
    is_string = False

    for key in dict.keys():
        seen_key = True
        is_string = (all_lower or all_upper) and isinstance(key, str)
        all_lower = all_lower and is_string and key.islower()
        all_upper = all_upper and is_string and key.isupper()

    return seen_key and (all_lower or all_upper)


empty_result = check_dict_case({})
lower_result = check_dict_case({"a": 1, "b2": 2})
upper_result = check_dict_case({"STATE": 1, "ZIP": 2})
mixed_result = check_dict_case({"a": 1, "B": 2})
late_mixed_result = check_dict_case({"A": 1, "B": 2, "c": 3})
late_nonstr_result = check_dict_case({"a": 1, "b": 2, 8: 3})
uncased_result = check_dict_case({"123": 1})
