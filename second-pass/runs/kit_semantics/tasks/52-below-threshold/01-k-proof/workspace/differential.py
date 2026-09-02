from itertools import product

from solution import below_threshold


def oracle(values, threshold):
    return all(value < threshold for value in values)


elements = (-3, -1, 0, 2, 5, False, True, -2.5, 0.5, 4.5)
thresholds = range(-3, 4)
checked = 0
mismatches = []

for length in range(5):
    for values in product(elements, repeat=length):
        for threshold in thresholds:
            expected = oracle(values, threshold)
            actual = below_threshold(list(values), threshold)
            checked += 1
            if actual != expected:
                mismatches.append((values, threshold, expected, actual))

print(f"checked={checked} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:10])
