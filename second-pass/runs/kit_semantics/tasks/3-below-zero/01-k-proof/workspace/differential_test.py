from itertools import product
from random import Random

from solution import below_zero


def oracle(operations):
    return any(sum(operations[:end]) < 0 for end in range(1, len(operations) + 1))


cases = 0
mismatches = 0

for length in range(7):
    for values in product(range(-3, 4), repeat=length):
        operations = list(values)
        cases += 1
        mismatches += below_zero(operations) != oracle(operations)

rng = Random(20260731)
for _ in range(2000):
    operations = [rng.randint(-100, 100) for _ in range(rng.randint(0, 40))]
    cases += 1
    mismatches += below_zero(operations) != oracle(operations)

print(f"DIFFERENTIAL_CASES={cases} MISMATCHES={mismatches}")
raise SystemExit(1 if mismatches else 0)
