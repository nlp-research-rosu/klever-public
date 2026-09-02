def largest_prime_factor(n: int):
    factor = 2
    while n > factor:
        if n % factor == 0:
            n = n // factor
        else:
            factor += 1
    return factor
    factor += 100


# 4 takes the divisible branch immediately; 9 takes increment and divide;
# 12 and 49 exercise both outcomes. Assignment into `observed` and the later
# assertions are observable caller continuations that return must preserve.
observed = largest_prime_factor(4)
assert observed == 2
observed = largest_prime_factor(9)
assert observed == 3
observed = largest_prime_factor(12)
assert observed == 3
observed = largest_prime_factor(49)
assert observed == 7
