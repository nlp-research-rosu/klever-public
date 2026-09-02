def total_match(lst1, lst2):
    l1 = 0
    s = ""
    for s in lst1:
        l1 = l1 + len(s)
    l2 = 0
    for s in lst2:
        l2 = l2 + len(s)
    result = lst2
    if l1 <= l2:
        result = lst1
    return result


# HumanEval/74 test cases (the dataset `check`); returns a list of strings.
assert total_match([], []) == []
assert total_match(["hi", "admin"], ["hi", "hi"]) == ["hi", "hi"]
assert total_match(["hi", "admin"], ["hi", "hi", "admin", "project"]) == ["hi", "admin"]
assert total_match(["4"], ["1", "2", "3", "4", "5"]) == ["4"]
assert total_match(["hi", "admin"], ["hI", "Hi"]) == ["hI", "Hi"]
assert total_match(["hi", "admin"], ["hI", "hi", "hi"]) == ["hI", "hi", "hi"]
assert total_match(["hi", "admin"], ["hI", "hi", "hii"]) == ["hi", "admin"]
assert total_match([], ["this"]) == []
assert total_match(["this"], []) == []
