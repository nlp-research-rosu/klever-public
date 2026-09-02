def no_even_digit(n):
    if n == 0:
        return True
    if n % 2 == 0:
        return False
    return no_even_digit(n // 10)


def unique_digits(x):
    return sorted([n for n in x if no_even_digit(n)])
