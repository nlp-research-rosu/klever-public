def largest_prime_factor(n: int):
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            n = n // factor
        else:
            factor = factor + 1
    return n
