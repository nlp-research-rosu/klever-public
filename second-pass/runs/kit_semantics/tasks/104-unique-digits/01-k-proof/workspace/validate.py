"""Deterministic differential tests against an independent string oracle."""

import random

from solution import unique_digits


def oracle(values):
    return sorted(
        value
        for value in values
        if all(digit in "13579" for digit in str(value))
    )


cases = [
    [],
    [15, 33, 1422, 1],
    [152, 323, 1422, 10],
    [7, 97531, 246, 111],
    [1, 3, 5, 7, 9],
    [2, 4, 6, 8, 10],
]

boundary_values = list(range(1, 1001)) + [
    1111,
    13579,
    97531,
    99999,
    10101,
    123456789,
    999999999,
]
cases.extend([value] for value in boundary_values)

rng = random.Random(20260725)
for _ in range(500):
    cases.append(
        [rng.randint(1, 1_000_000_000) for _ in range(rng.randint(0, 12))]
    )

mismatches = []
for values in cases:
    actual = unique_digits(values)
    expected = oracle(values)
    if actual != expected:
        mismatches.append((values, actual, expected))

print(f"differential cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:5]:
        print(mismatch)
    raise SystemExit(1)
