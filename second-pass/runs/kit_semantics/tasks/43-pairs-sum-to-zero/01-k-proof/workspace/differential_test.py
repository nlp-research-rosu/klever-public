from itertools import product

from solution import pairs_sum_to_zero


def oracle(values):
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] + values[j] == 0:
                return True
    return False


tested = 0
mismatches = []
for length in range(6):
    for values in product(range(-2, 3), repeat=length):
        data = list(values)
        expected = oracle(data)
        actual = pairs_sum_to_zero(data)
        tested += 1
        if actual != expected:
            mismatches.append((data, expected, actual))

print(f"DIFFERENTIAL_CASES={tested}")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
