def largest_prime_factor(n: int):
    factor = 2
    while n > factor:
        if n % factor == 0:
            n = n // factor
        else:
            factor += 1
    return factor


assert largest_prime_factor(13195) == 29
assert largest_prime_factor(2048) == 2
assert largest_prime_factor(4) == 2
assert largest_prime_factor(6) == 3
assert largest_prime_factor(12) == 3
assert largest_prime_factor(49) == 7
