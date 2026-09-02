import itertools
import random

from solution import sort_third


def oracle(source):
    expected = source[:]
    expected[::3] = sorted(source[::3])
    return expected


cases = [[]]
for length in range(1, 9):
    cases.extend(
        list(values)
        for values in itertools.islice(
            itertools.product(range(-2, 3), repeat=length),
            40,
        )
    )

rng = random.Random(20260729)
for length in range(0, 31):
    for _ in range(20):
        cases.append([rng.randint(-100, 100) for _ in range(length)])

cases.extend([
    list(""),
    list("a"),
    list("sortthird"),
    list("zyxwvutsrqpon"),
])

mismatches = []
for source in cases:
    actual = sort_third(source)
    expected = oracle(source)
    if actual != expected:
        mismatches.append((source, actual, expected))

assert not mismatches, mismatches[:3]
print(f"differential: {len(cases)} cases, 0 mismatches")
