"""Deterministic CPython differential check for solution.incr_list."""

from itertools import product

from solution import incr_list


VALUES = (-3, 0, 4, False, True, -2.5, 0.5, 3.0)
CASES = [[]]
for length in range(1, 4):
    CASES.extend([list(items) for items in product(VALUES, repeat=length)])

mismatches = []
for case in CASES:
    expected = [value + 1 for value in case]
    actual = incr_list(case)
    if actual != expected:
        mismatches.append((case, expected, actual))

print(f"cases={len(CASES)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(mismatch)
    raise SystemExit(1)
