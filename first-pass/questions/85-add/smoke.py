def add(lst):
    result = 0
    i = 0
    e = 0
    for e in lst:
        if i % 2 == 1:
            if e % 2 == 0:
                result = result + e
        i = i + 1
    return result


# HumanEval/85 test cases (the dataset `check`); returns an int.
assert add([4, 88]) == 88
assert add([4, 5, 6, 7, 2, 122]) == 122
assert add([4, 0, 6, 7]) == 0
assert add([4, 4, 6, 8]) == 12
