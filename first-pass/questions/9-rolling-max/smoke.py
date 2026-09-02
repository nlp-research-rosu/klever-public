def rolling_max(numbers):
    result = []
    m = 0
    first = True
    n = 0
    for n in numbers:
        if first:
            m = n
            first = False
        else:
            if n > m:
                m = n
        result = result + [m]
    return result


# HumanEval/9 test cases (the dataset `check`); returns a list.
assert rolling_max([]) == []
assert rolling_max([1, 2, 3, 4]) == [1, 2, 3, 4]
assert rolling_max([4, 3, 2, 1]) == [4, 4, 4, 4]
assert rolling_max([3, 2, 3, 100, 3]) == [3, 3, 3, 100, 100]
