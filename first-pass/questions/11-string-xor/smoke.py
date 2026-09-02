def string_xor(a, b):
    result = ""
    x = ""
    y = ""
    for x, y in zip(a, b):
        if x == y:
            result = result + "0"
        else:
            result = result + "1"
    return result


# HumanEval/11 test cases (the dataset `check`); returns a string.
assert string_xor("111000", "101010") == "010010"
assert string_xor("1", "1") == "0"
assert string_xor("0101", "0000") == "0101"
