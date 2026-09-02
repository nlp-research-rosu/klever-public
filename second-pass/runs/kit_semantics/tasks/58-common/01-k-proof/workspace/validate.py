from itertools import product

from solution import common


def oracle(left, right):
    return sorted(set(left).intersection(set(right)))


mismatches = []
pair_count = 0

for values in ((-1, 0, 1), ("a", "b", "c")):
    lists = [
        list(items)
        for size in range(4)
        for items in product(values, repeat=size)
    ]
    pair_count += len(lists) * len(lists)
    for left in lists:
        for right in lists:
            actual = common(left, right)
            expected = oracle(left, right)
            if actual != expected:
                mismatches.append((left, right, actual, expected))

print(
    "CPython differential:",
    f"{pair_count} pairs,",
    f"{len(mismatches)} mismatches",
)

if mismatches:
    raise AssertionError(mismatches[:5])
