#!/usr/bin/env python3
"""Finite independent validation of solution.even_odd_count."""

from solution import even_odd_count


def oracle(num):
    digits = str(abs(num))
    even = sum(1 for digit in digits if int(digit) % 2 == 0)
    odd = len(digits) - even
    return even, odd


def main():
    inputs = list(range(-10000, 10001))
    inputs += [
        -(10**50 + 24680),
        -(10**30),
        10**30,
        10**50 + 13579,
    ]
    mismatches = []
    for num in inputs:
        actual = even_odd_count(num)
        expected = oracle(num)
        if actual != expected:
            mismatches.append((num, actual, expected))
    print(f"differential cases: {len(inputs)}; mismatches: {len(mismatches)}")
    if mismatches:
        raise AssertionError(mismatches[:10])


if __name__ == "__main__":
    main()
