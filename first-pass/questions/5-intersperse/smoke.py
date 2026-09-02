def intersperse(numbers, delimeter):
    result = []
    first = True
    n = 0
    for n in numbers:
        if first:
            result = result + [n]
            first = False
        else:
            result = result + [delimeter, n]
    return result


# HumanEval/5 test cases (the dataset `check`); returns a list.
assert intersperse([], 7) == []
assert intersperse([5, 6, 3, 2], 8) == [5, 8, 6, 8, 3, 8, 2]
assert intersperse([2, 2, 2], 2) == [2, 2, 2, 2, 2]
