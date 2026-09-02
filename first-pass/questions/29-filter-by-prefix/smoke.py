def filter_by_prefix(strings, prefix):
    result = []
    x = ""
    for x in strings:
        if x.startswith(prefix):
            result = result + [x]
    return result


# HumanEval/29 test cases (the dataset `check`); returns a list of strings.
assert filter_by_prefix([], "john") == []
assert filter_by_prefix(["xxx", "asd", "xxy", "john doe", "xxxAAA", "xxx"], "xxx") == ["xxx", "xxxAAA", "xxx"]
