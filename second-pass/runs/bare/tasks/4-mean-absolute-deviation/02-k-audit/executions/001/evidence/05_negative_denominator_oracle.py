#!/usr/bin/env python3
"""Mathematical oracle for the accepted negative-denominator K witness."""

from fractions import Fraction

values = [Fraction(3, -1), Fraction(1, -1)]
mean = sum(values, Fraction(0, 1)) / len(values)
mad = sum((abs(value - mean) for value in values), Fraction(0, 1)) / len(values)

print(f"semantic input terms: nums(rat(3,-1),rat(1,-1))")
print(f"mathematical rational values: {values!r}")
print(f"mathematical mean: {mean}")
print(f"mathematical MAD: {mad}")
assert mad == 1
