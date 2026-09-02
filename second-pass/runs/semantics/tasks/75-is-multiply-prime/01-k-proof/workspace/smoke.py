def is_multiply_prime(a):
    """Return whether a has exactly three prime factors, with multiplicity."""
    factor_count = 0
    factor = 2

    while factor * factor <= a:
        if a % factor == 0:
            factor_count += 1
            a //= factor
        else:
            factor += 1

    if a > 1:
        factor_count += 1

    return factor_count == 3


assert is_multiply_prime(30)
assert is_multiply_prime(8)
assert not is_multiply_prime(10)
assert not is_multiply_prime(-7)
