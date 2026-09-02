import math

from solution import special_factorial


def oracle(n):
    return math.prod(math.factorial(k) for k in range(1, n + 1))


mismatches = []
for value in range(1, 21):
    actual = special_factorial(value)
    expected = oracle(value)
    if actual != expected:
        mismatches.append((value, actual, expected))

print("oracle_1_to_6=" + str([oracle(value) for value in range(1, 7)]))
print("inputs=1..20 mismatches=" + str(len(mismatches)))
if mismatches:
    print(mismatches)
    raise SystemExit(1)
