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


unicode_lower_result = check_dict_case({"é": 1})
