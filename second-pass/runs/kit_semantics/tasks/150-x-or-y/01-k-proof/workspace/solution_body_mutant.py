def x_or_y(n, x, y):
    if n < 2:
        return y

    i = 2
    result = y
    while i < n:
        if n % i == 0:
            result = y
        i = i + 1

    return result
