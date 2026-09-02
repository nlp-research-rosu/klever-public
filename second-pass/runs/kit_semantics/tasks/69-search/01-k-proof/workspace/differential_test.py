from itertools import product
from random import Random

from solution import search


def contract_oracle(values):
    qualifying = [
        value
        for value in set(values)
        if values.count(value) >= value
    ]
    return max(qualifying) if qualifying else -1


cases = []
for length in range(1, 7):
    cases.extend(list(values) for values in product(range(1, 6), repeat=length))

rng = Random(20260729)
for _ in range(500):
    length = rng.randint(1, 30)
    cases.append([rng.randint(1, 30) for _ in range(length)])

mismatches = []
for values in cases:
    expected = contract_oracle(values)
    actual = search(values)
    if actual != expected:
        mismatches.append((values, expected, actual))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(mismatch)
    raise SystemExit(1)
