from itertools import product

from solution import compare_one


def oracle(a, b):
    av = float(a.replace(",", ".")) if isinstance(a, str) else a
    bv = float(b.replace(",", ".")) if isinstance(b, str) else b
    if av == bv:
        return None
    return a if av > bv else b


values = [
    -100,
    -2,
    0,
    1,
    100,
    -3.5,
    -0.0,
    0.25,
    2.5,
    "-100",
    "-3,5",
    "-0.0",
    "0",
    "0,25",
    "1.00",
    "2,5",
    "100",
]

mismatches = []
for a, b in product(values, repeat=2):
    actual = compare_one(a, b)
    expected = oracle(a, b)
    if type(actual) is not type(expected) or actual != expected:
        mismatches.append((a, b, actual, expected))

print(f"cases={len(values) ** 2} mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
