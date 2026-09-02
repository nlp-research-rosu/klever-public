def no_divisor(n, d):
    if d * d > n:
        return True
    if n % d == 0:
        return False
    return no_divisor(n, d + 1)


def is_prime(n):
    if n < 2:
        return False
    return no_divisor(n, 2)
