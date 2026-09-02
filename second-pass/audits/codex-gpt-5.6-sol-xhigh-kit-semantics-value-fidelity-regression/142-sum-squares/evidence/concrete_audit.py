def sum_squares(lst):
    total = 0
    index = 0
    value = 0
    for value in lst:
        if index % 3 == 0:
            total += value * value
        elif index % 4 == 0:
            total += value * value * value
        else:
            total += value
        index += 1
    return total


assert sum_squares([]) == 0
assert sum_squares([1, 2, 3]) == 6
assert sum_squares([-1, -5, 2, -1, -5]) == -126
assert sum_squares([-3]) == 9
assert sum_squares([2, -2, 3, -4]) == 21
assert sum_squares([2, -2, 3, -4, -5]) == -104
assert sum_squares([1, 1, 1, 1, 1, 1, 1, 1, -2]) == 0
assert sum_squares([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -3]) == 21
