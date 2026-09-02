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
