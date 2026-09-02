def x_or_y(n, x, y):
    if n < 2:
        return y
    for divisor in range(2, n):
        if n % divisor == 0:
            return y
    return x


assert x_or_y(7, 34, 12) == 34
assert x_or_y(15, 8, 5) == 5
assert x_or_y(-3, 11, 22) == 22
assert x_or_y(0, 11, 22) == 22
assert x_or_y(1, 11, 22) == 22
assert x_or_y(2, 11, 22) == 11
assert x_or_y(3, 11, 22) == 11
assert x_or_y(4, 11, 22) == 22
assert x_or_y(9, 11, 22) == 22
assert x_or_y(49, 11, 22) == 22
assert x_or_y(97, 11, 22) == 11
