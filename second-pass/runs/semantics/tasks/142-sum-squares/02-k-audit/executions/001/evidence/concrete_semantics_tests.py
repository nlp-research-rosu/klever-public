def sum_squares(lst):
    total = 0
    index = 0
    for value in lst:
        if index % 3 == 0:
            total += value * value
        else:
            if index % 4 == 0:
                total += value * value * value
            else:
                total += value
        index += 1
    return total


assert sum_squares([]) == 0
assert sum_squares([1]) == 1
assert sum_squares([1, 2, 3]) == 6
assert sum_squares([-1, -5, 2, -1, -5]) == -126
assert sum_squares([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) == 1231
assert sum_squares([2, -3, 4, -5, 6, -7, 8, -9, 10, -11, 12, -13, 14]) == 1610
