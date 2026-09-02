def is_simple_power(x, n):
    if x == 1:
        return True
    if n == 0:
        return x == 0
    if n == 1:
        return False
    if n == -1:
        return x == -1
    if x == 0:
        return False
    while x % n == 0:
        x = x // n
    return x == 1
