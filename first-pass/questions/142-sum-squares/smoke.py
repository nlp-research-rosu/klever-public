def sum_squares(lst):
    result = 0
    i = 0
    e = 0
    for e in lst:
        if i % 3 == 0:
            result = result + e * e
        else:
            if i % 4 == 0:
                result = result + e * e * e
            else:
                result = result + e
        i = i + 1
    return result


# HumanEval/142 test cases (the dataset `check`); returns an int.
assert sum_squares([1, 2, 3]) == 6
assert sum_squares([1, 4, 9]) == 14
assert sum_squares([]) == 0
assert sum_squares([1, 1, 1, 1, 1, 1, 1, 1, 1]) == 9
assert sum_squares([-1, -1, -1, -1, -1, -1, -1, -1, -1]) == -3
assert sum_squares([0]) == 0
assert sum_squares([-1, -5, 2, -1, -5]) == -126
assert sum_squares([-56, -99, 1, 0, -2]) == 3030
assert sum_squares([-1, 0, 0, 0, 0, 0, 0, 0, -1]) == 0
