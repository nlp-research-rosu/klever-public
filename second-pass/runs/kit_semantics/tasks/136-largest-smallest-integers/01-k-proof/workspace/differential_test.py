from itertools import product

from solution import largest_smallest_integers


def oracle(values):
    negatives = [value for value in values if value < 0]
    positives = [value for value in values if value > 0]
    return (
        max(negatives) if negatives else None,
        min(positives) if positives else None,
    )


checked = 0
mismatches = []
alphabet = range(-3, 4)

for length in range(6):
    for values in product(alphabet, repeat=length):
        actual = largest_smallest_integers(list(values))
        expected = oracle(values)
        checked += 1
        if actual != expected:
            mismatches.append((values, actual, expected))

print(f"checked={checked} mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
