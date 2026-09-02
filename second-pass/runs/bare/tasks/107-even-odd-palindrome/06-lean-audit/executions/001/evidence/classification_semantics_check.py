#!/usr/bin/env python3
from __future__ import annotations


def frozen_program(n: int) -> tuple[int, int]:
    if n < 10:
        even = n // 2
        odd = n - even
        return even, odd

    even = 4
    odd = 5
    pairs = n // 11
    if pairs > 9:
        pairs = 9
    even = even + pairs // 2
    odd = odd + pairs - pairs // 2

    if n >= 101:
        lead = n // 100
        if lead > 9:
            lead = 9
            extra = 10
        else:
            middle = (n // 10) % 10
            candidate = lead * 101 + middle * 10
            extra = middle
            if candidate <= n:
                extra = extra + 1

        previous = lead - 1
        even_leads = previous // 2
        odd_leads = previous - even_leads
        even = even + even_leads * 10
        odd = odd + odd_leads * 10
        if lead % 2 == 0:
            even = even + extra
        else:
            odd = odd + extra

    return even, odd


def k_reverse_digits(n: int) -> int:
    if 0 <= n < 10:
        return n
    if 10 <= n < 100:
        return (n % 10) * 10 + n // 10
    if 100 <= n < 1000:
        return (n % 10) * 100 + ((n // 10) % 10) * 10 + n // 100
    if n == 1000:
        return 1
    raise ValueError("outside the frozen definition domain")


def k_indicator(n: int) -> tuple[int, int]:
    palindrome = k_reverse_digits(n) == n
    return (
        int(palindrome and n % 2 == 0),
        int(palindrome and n % 2 == 1),
    )


def independent_oracle(n: int) -> tuple[int, int]:
    palindromes = [value for value in range(1, n + 1) if str(value) == str(value)[::-1]]
    return (
        sum(value % 2 == 0 for value in palindromes),
        sum(value % 2 == 1 for value in palindromes),
    )


indicator_totals = [0, 0]
mismatches: list[tuple[int, object, object]] = []
for n in range(1, 1001):
    reversed_oracle = int(str(n)[::-1])
    if k_reverse_digits(n) != reversed_oracle:
        mismatches.append((n, k_reverse_digits(n), reversed_oracle))
    even_step, odd_step = k_indicator(n)
    indicator_totals[0] += even_step
    indicator_totals[1] += odd_step
    program = frozen_program(n)
    oracle = independent_oracle(n)
    if program != tuple(indicator_totals):
        mismatches.append((n, program, tuple(indicator_totals)))
    if program != oracle:
        mismatches.append((n, program, oracle))

assert not mismatches, mismatches[:10]
assert frozen_program(1) != frozen_program(2)
assert frozen_program(10) != frozen_program(11)
assert frozen_program(100) != frozen_program(101)
assert frozen_program(998) != frozen_program(999)

print("SEMANTICS_ORACLE_CHECK: PASS")
print("domain=1..1000")
print("reverseDigits_mismatches=0")
print("indicator_cumulative_mismatches=0")
print("frozen_program_vs_decimal_oracle_mismatches=0")
for n in (1, 3, 9, 10, 11, 12, 99, 100, 101, 111, 999, 1000):
    print(f"n={n} program={frozen_program(n)} oracle={independent_oracle(n)}")
