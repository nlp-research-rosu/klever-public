#!/usr/bin/env python3
"""Ground witness for the factorial-update body mutation."""

from math import factorial


def mutated(n: int) -> list[int]:
    result: list[int] = []
    factorial_accumulator = 1
    total = 0
    i = 1
    while i <= n:
        factorial_accumulator = factorial_accumulator + i
        total = total + i
        result.append(factorial_accumulator if i % 2 == 0 else total)
        i += 1
    return result


n = 2
contract = [
    factorial(i) if i % 2 == 0 else i * (i + 1) // 2
    for i in range(1, n + 1)
]
actual = mutated(n)
print(f"satisfying input n={n}")
print(f"mutated_body_result={actual}")
print(f"contract_result={contract}")
print(f"false_conclusion_witness={actual != contract}")
