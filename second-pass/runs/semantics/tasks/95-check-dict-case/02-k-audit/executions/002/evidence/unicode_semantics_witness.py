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


# Python evaluates this to True because U+00E9 is a lowercase Unicode letter.
# The supplied K semantics classifies only ASCII A-Z/a-z, so this assertion is
# expected to end in AssertionError and witnesses the language-model gap.
assert check_dict_case({"é": 0}) == True
