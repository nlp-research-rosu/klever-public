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


# Prompt examples and empty boundary.
assert sum_squares([1, 2, 3]) == 6
assert sum_squares([]) == 0
assert sum_squares([-1, -5, 2, -1, -5]) == -126

# Cross a full lcm(3,4) index period; at index 12, square has precedence.
assert sum_squares([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]) == 48

# Negative/zero/positive values while exercising every branch residue.
assert sum_squares([-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == 279

# Mathematical integers are unbounded in the modeled domain.
assert sum_squares([100000000000000000000, -1, 0, 2, -3]) == 9999999999999999999999999999999999999976
