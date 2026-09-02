def longest(strings):
    best = None
    s = ""
    for s in strings:
        if best is None or len(s) > len(best):
            best = s
    return best


# HumanEval/12 test cases (the dataset `check`); returns a string or None.
assert longest([]) is None
assert longest(["x", "y", "z"]) == "x"
assert longest(["x", "yyy", "zzzz", "www", "kkkk", "abc"]) == "zzzz"
