def multiply(a, b):
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    return (a % 10) * (b % 10)
