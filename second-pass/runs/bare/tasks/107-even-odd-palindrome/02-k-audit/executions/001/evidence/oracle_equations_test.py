#!/usr/bin/env python3
"""Check the proof-side digit equations against the trusted canonical oracle."""

from canonical import even_odd_palindrome


def reverse_digits_equation(n: int) -> int:
    if 0 <= n < 10:
        return n
    if 10 <= n < 100:
        return (n % 10) * 10 + n // 10
    if 100 <= n < 1000:
        return (n % 10) * 100 + ((n // 10) % 10) * 10 + n // 100
    if n == 1000:
        return 1
    raise ValueError(n)


even = 0
odd = 0
mismatches = []
for n in range(1, 1001):
    palindrome = reverse_digits_equation(n) == n
    even += int(palindrome and n % 2 == 0)
    odd += int(palindrome and n % 2 == 1)
    expected = even_odd_palindrome(n)
    observed = (even, odd)
    if expected != observed:
        mismatches.append((n, expected, observed))

print(f"domain=1..1000 equation_checks=1000 mismatches={len(mismatches)}")
print(f"final_counts={(even, odd)}")
if mismatches:
    print(f"first_mismatches={mismatches[:20]}")
raise SystemExit(1 if mismatches else 0)
