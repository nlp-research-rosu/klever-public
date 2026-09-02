def derivative(xs):
    result = []
    i = 0
    x = 0
    for x in xs:
        if i >= 1:
            result = result + [i * x]
        i = i + 1
    return result


# HumanEval/62 test cases (the dataset `check`); returns a list.
assert derivative([3, 1, 2, 4, 5]) == [1, 4, 12, 20]
assert derivative([1, 2, 3]) == [2, 6]
assert derivative([3, 2, 1]) == [2, 2]
assert derivative([3, 2, 1, 0, 4]) == [2, 2, 0, 16]
assert derivative([1]) == []
