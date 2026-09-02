def all_prefixes(string):
    result = []
    acc = ""
    c = ""
    for c in string:
        acc = acc + c
        result = result + [acc]
    return result


# HumanEval/14 test cases (the dataset `check`); returns a list of strings.
assert all_prefixes("") == []
assert all_prefixes("asdfgh") == ["a", "as", "asd", "asdf", "asdfg", "asdfgh"]
assert all_prefixes("WWW") == ["W", "WW", "WWW"]
