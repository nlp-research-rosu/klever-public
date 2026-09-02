def x_or_y(n, x, y):
    if n < 2:
        return y
    for divisor in range(2, n):
        if n % divisor == 0:
            return y
    return x


assert x_or_y(7, 34, 12) == 34
assert x_or_y(15, 8, 5) == 5
assert x_or_y(1, 7, 9) == 9
assert x_or_y(2, 11, 13) == 11
assert x_or_y(0, 4, 6) == 6
assert x_or_y(97, -2, 10) == -2
assert x_or_y(49, 3, 4) == 4
