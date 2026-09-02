def largest_prime_factor(n: int):
    factor = 2
    while n > factor:
        if n % factor == 0:
            n = n // factor
        else:
            factor = factor + 1
    return n


documented_13195 = largest_prime_factor(13195)
documented_2048 = largest_prime_factor(2048)
boundary_4 = largest_prime_factor(4)
nondivisible_branch_15 = largest_prime_factor(15)
repeated_division_16384 = largest_prime_factor(16384)
