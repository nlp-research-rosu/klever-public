def largest_prime_factor(n: int):
    factor = 2
    while n > factor:
        if n % factor == 0:
            n = n // factor
        else:
            factor = factor + 1
    return n


example_13195 = largest_prime_factor(13195)
example_2048 = largest_prime_factor(2048)
boundary_4 = largest_prime_factor(4)
