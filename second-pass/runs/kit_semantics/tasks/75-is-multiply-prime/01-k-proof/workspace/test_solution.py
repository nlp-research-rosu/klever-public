from solution import is_multiply_prime


def oracle(a):
    factors = 0
    divisor = 2
    remaining = a
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors += 1
            remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors += 1
    return factors == 3


checked = 0
for value in range(-100, 100):
    expected = oracle(value)
    actual = is_multiply_prime(value)
    if actual != expected:
        raise AssertionError((value, expected, actual))
    checked += 1

assert is_multiply_prime(30) is True
print("checked:", checked, "mismatches:", 0)
