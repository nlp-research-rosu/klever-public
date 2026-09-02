def concatenate(strings):
    result = ""
    s = ""
    for s in strings:
        result = result + s
    return result


# HumanEval/28 test cases (the dataset `check`); returns a string.
assert concatenate([]) == ""
assert concatenate(["x", "y", "z"]) == "xyz"
assert concatenate(["x", "y", "z", "w", "k"]) == "xyzwk"
