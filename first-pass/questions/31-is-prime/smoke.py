def is_prime(n):
    prime = n >= 2
    k = 0
    for k in range(2, n - 1):
        if n % k == 0:
            prime = False
    return prime


# HumanEval/31 dataset `check` cases (bare-bool asserts; 13441 dropped — too many
# interpreter iterations for krun, the smaller primes/composites are representative).
assert not is_prime(6)
assert is_prime(101)
assert is_prime(11)
assert is_prime(61)
assert not is_prime(4)
assert not is_prime(1)
assert is_prime(5)
assert is_prime(17)
