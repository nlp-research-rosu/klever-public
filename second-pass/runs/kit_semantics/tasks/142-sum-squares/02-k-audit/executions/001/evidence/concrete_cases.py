def sum_squares(lst):
    result = 0
    index = 0
    value = 0
    for value in lst:
        if index % 3 == 0:
            result += value * value
        elif index % 4 == 0:
            result += value * value * value
        else:
            result += value
        index += 1
    return result


# Prompt examples.
assert sum_squares([1, 2, 3]) == 6
assert sum_squares([]) == 0
assert sum_squares([-1, -5, 2, -1, -5]) == -126

# Independently selected branch-boundary witnesses.
assert sum_squares([2, 3, 4, 5, 2]) == 44
assert sum_squares([0, 0, 0, 0, -2]) == -8
assert sum_squares([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]) == 4
assert sum_squares([-7]) == 49
