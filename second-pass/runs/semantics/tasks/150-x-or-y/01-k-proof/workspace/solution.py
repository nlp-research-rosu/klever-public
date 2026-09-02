def x_or_y(n, x, y):
    if n < 2:
        return y
    for divisor in range(2, n):
        if n % divisor == 0:
            return y
    return x
