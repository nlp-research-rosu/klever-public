def x_or_y(n, x, y):
    if n < 2:
        return y
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return y
        divisor = divisor + 1
    return x
