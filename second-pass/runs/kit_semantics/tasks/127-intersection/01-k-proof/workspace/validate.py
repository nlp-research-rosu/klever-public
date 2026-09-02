from math import isqrt

from solution import intersection


def oracle_is_prime(n):
    if n < 2:
        return False
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def oracle_intersection(interval1, interval2):
    length = min(interval1[1], interval2[1]) - max(
        interval1[0], interval2[0]
    )
    return "YES" if oracle_is_prime(length) else "NO"


def proof_equation_scan(seen, n, divisor):
    if seen:
        return True
    if divisor < 2:
        divisor = 2
    while divisor < n:
        if n % divisor == 0:
            return True
        divisor += 1
    return False


def independent_scan_oracle(seen, n, divisor):
    if seen:
        return True
    lower = max(2, divisor)
    return any(n % candidate == 0 for candidate in range(lower, n))


intervals = [
    (start, end)
    for start in range(-6, 7)
    for end in range(start, 7)
]
program_mismatches = []
for interval1 in intervals:
    for interval2 in intervals:
        actual = intersection(interval1, interval2)
        expected = oracle_intersection(interval1, interval2)
        if actual != expected:
            program_mismatches.append((interval1, interval2, actual, expected))

summary_mismatches = []
summary_cases = 0
for seen in (False, True):
    for n in range(-10, 101):
        for divisor in range(-3, 104):
            summary_cases += 1
            proof_value = proof_equation_scan(seen, n, divisor)
            oracle_value = independent_scan_oracle(seen, n, divisor)
            if proof_value != oracle_value:
                summary_mismatches.append(
                    (seen, n, divisor, proof_value, oracle_value)
                )

assert not program_mismatches, program_mismatches[:5]
assert not summary_mismatches, summary_mismatches[:5]

print(
    "validation:"
    f" program_cases={len(intervals) ** 2}"
    f" program_mismatches={len(program_mismatches)}"
    f" summary_cases={summary_cases}"
    f" summary_mismatches={len(summary_mismatches)}"
)
