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


# Prompt examples and empty input.
assert sum_squares([]) == 0
assert sum_squares([1, 2, 3]) == 6
assert sum_squares([-1, -5, 2, -1, -5]) == -126

# Indices 0..12 cover: multiple of 3; multiple of 4 but not 3; neither;
# and the overlap at 12 where the multiple-of-3 branch must take precedence.
assert sum_squares([2, 3, 4, 5, 6, 7, 8, 9, 10]) == 1332
assert sum_squares([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]) == 90

# Unbounded mathematical integer behavior used by the symbolic theorem.
assert sum_squares([100000000000000000000, -2, 3, 4, -5]) == (
    10000000000000000000000000000000000000000 - 2 + 3 + 16 - 125
)
