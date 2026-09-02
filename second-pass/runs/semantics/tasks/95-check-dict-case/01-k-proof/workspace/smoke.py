def check_dict_case(dict):
    has_key = False
    all_lower = True
    all_upper = True
    key = None

    for key in dict.keys():
        has_key = True
        if not isinstance(key, str):
            all_lower = False
            all_upper = False
        else:
            if not key.islower():
                all_lower = False
            if not key.isupper():
                all_upper = False

    return has_key and (all_lower or all_upper)


assert check_dict_case({"a": "apple", "b": "banana"}) == True
assert check_dict_case({"a": "apple", "A": "banana", "B": "banana"}) == False
assert check_dict_case({"a": "apple", 8: "banana"}) == False
assert check_dict_case({"Name": "John", "Age": "36", "City": "Houston"}) == False
assert check_dict_case({"STATE": "NC", "ZIP": "12345"}) == True
assert check_dict_case({}) == False
assert check_dict_case({"123": "digits"}) == False
