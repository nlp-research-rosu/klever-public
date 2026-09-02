from itertools import combinations, product

from solution import triples_sum_to_zero


def oracle(values):
    return any(sum(triple) == 0 for triple in combinations(values, 3))


checked = 0
mismatches = 0
for length in range(7):
    for values in product(range(-3, 4), repeat=length):
        expected = oracle(values)
        actual = triples_sum_to_zero(list(values))
        checked += 1
        if actual != expected:
            mismatches += 1
            print("MISMATCH", values, actual, expected)

print(f"DIFFERENTIAL_CASES={checked}")
print(f"MISMATCHES={mismatches}")
assert mismatches == 0
