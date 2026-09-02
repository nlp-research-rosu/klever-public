def check_dict_case(dict):
    if not dict:
        return False

    lower = True
    upper = True
    for key in dict:
        if not isinstance(key, str):
            return False
        if not key.islower():
            lower = False
        if not key.isupper():
            upper = False

    return lower or upper
