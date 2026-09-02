def x_or_y(n, x, y):
    if n < 2:
        return y
    for divisor in range(2, n):
        if n % divisor == 0:
            return y
    return x


# Prompt examples.
assert x_or_y(7, 34, 12) == 34
assert x_or_y(15, 8, 5) == 5

# Boundary and branch-sensitive cases.
assert x_or_y(-3, 1, 2) == 2
assert x_or_y(0, 3, 4) == 4
assert x_or_y(1, 5, 6) == 6
assert x_or_y(2, 7, 8) == 7
assert x_or_y(4, 9, 10) == 10
assert x_or_y(9, 11, 12) == 12
assert x_or_y(97, 13, 14) == 13
assert x_or_y(49, 15, 16) == 16
