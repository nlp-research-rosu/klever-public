from math import isqrt

from solution import prime_fib


def oracle_is_prime(value):
    if value < 2:
        return False
    for divisor in range(2, isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def oracle_prime_fibs(limit):
    values = []
    a = 0
    b = 1
    while len(values) < limit:
        a, b = b, a + b
        if oracle_is_prime(a):
            values.append(a)
    return values


expected_examples = [2, 3, 5, 13, 89]
actual_examples = [prime_fib(n) for n in range(1, 6)]
assert actual_examples == expected_examples

oracle_values = oracle_prime_fibs(10)
actual_values = [prime_fib(n) for n in range(1, 11)]
assert actual_values == oracle_values

print("prompt examples:", actual_examples)
print("differential inputs: n=1..10")
print("oracle values:", oracle_values)
print("mismatches: 0")
