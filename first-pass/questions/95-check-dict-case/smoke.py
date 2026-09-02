def check_dict_case(d):
    keys = list(d.keys())
    n = len(keys)
    if n == 0:
        return False
    k0 = keys[0]
    if not isinstance(k0, str):
        return False
    if k0.isupper():
        first = 'upper'
    elif k0.islower():
        first = 'lower'
    else:
        return False
    if n == 1:
        return True
    k1 = keys[1]
    if not isinstance(k1, str):
        return False
    if first == 'upper':
        return k1.isupper()
    else:
        return k1.islower()


# Smoke checks — the HumanEval/95 dataset `check` cases (bare-bool asserts).
assert check_dict_case({"p": "pineapple", "b": "banana"})
assert not check_dict_case({"p": "pineapple", "A": "banana", "B": "banana"})
assert not check_dict_case({"p": "pineapple", 5: "banana", "a": "apple"})
assert not check_dict_case({"Name": "John", "Age": "36", "City": "Houston"})
assert check_dict_case({"STATE": "NC", "ZIP": "12345"})
assert check_dict_case({"fruit": "Orange", "taste": "Sweet"})
assert not check_dict_case({})
