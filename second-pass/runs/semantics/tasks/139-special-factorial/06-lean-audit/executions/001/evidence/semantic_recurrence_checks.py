#!/usr/bin/env python3
"""Ground checks for the two Stage 1 mathematical summary definitions."""

from functools import cache


def source_special_factorial(n: int) -> int:
    factorial = 1
    result = 1
    i = 1
    while i <= n:
        factorial *= i
        result *= factorial
        i += 1
    return result


@cache
def k_factorial(n: int) -> int:
    if n <= 0:
        return 1
    return k_factorial(n - 1) * n


@cache
def k_special_factorial(n: int) -> int:
    if n <= 0:
        return 1
    return k_special_factorial(n - 1) * k_factorial(n)


def mutated_factorial_base(n: int) -> int:
    result = 0
    for i in range(1, n + 1):
        result *= i
    return result


def mutated_factorial_step(n: int) -> int:
    return 1


def mutated_special_base(n: int) -> int:
    result = 0
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
        result *= factorial
    return result


def mutated_special_step(n: int) -> int:
    return 1


for n in range(-3, 11):
    nonpositive = n <= 0
    positive = n > 0
    assert nonpositive != positive
    observed = source_special_factorial(n)
    summary = k_special_factorial(n)
    assert observed == summary
    print(
        f"n={n:>2} source={observed:<16} "
        f"factorial={k_factorial(n):<10} summary={summary}"
    )

counterfactuals = {
    "factorial base 1 -> 0": mutated_factorial_base(4),
    "factorial step F(n-1)*n -> 1": mutated_factorial_step(4),
    "special base 1 -> 0": mutated_special_base(4),
    "special step S(n-1)*F(n) -> 1": mutated_special_step(4),
}
expected = source_special_factorial(4)
for mutation, value in counterfactuals.items():
    assert value != expected
    print(f"counterfactual rejected: {mutation}; got {value}, expected {expected}")

print("SUMMARY PASS: recurrences agree with source loop and all four rules are body-sensitive")
