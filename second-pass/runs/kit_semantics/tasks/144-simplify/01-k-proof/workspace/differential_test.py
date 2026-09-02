from fractions import Fraction
from random import Random

from solution import simplify


def oracle(x, n):
    a, b = (int(part) for part in x.split("/"))
    c, d = (int(part) for part in n.split("/"))
    return (Fraction(a, b) * Fraction(c, d)).denominator == 1


cases = [
    ("1/5", "5/1"),
    ("1/6", "2/1"),
    ("7/10", "10/2"),
    ("00012/0005", "00015/0004"),
    ("999999999999999999/7", "14/999999999999999999"),
]

for a in range(1, 21):
    for b in range(1, 21):
        for c in range(1, 21):
            for d in range(1, 21):
                cases.append((f"{a}/{b}", f"{c}/{d}"))

rng = Random(20260729)
for _ in range(1000):
    a, b, c, d = (rng.randrange(1, 10**30) for _ in range(4))
    cases.append(
        (
            f"{'0' * rng.randrange(4)}{a}/{'0' * rng.randrange(4)}{b}",
            f"{'0' * rng.randrange(4)}{c}/{'0' * rng.randrange(4)}{d}",
        )
    )

mismatches = [
    (x, n, simplify(x, n), oracle(x, n))
    for x, n in cases
    if simplify(x, n) != oracle(x, n)
]

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:10])
