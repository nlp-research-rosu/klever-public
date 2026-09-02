#!/usr/bin/env python3
"""Finite ground checks supporting the independent definitional reading."""

from __future__ import annotations


def source_behavior(numbers: list[int]) -> list[int]:
    # Independent executable reading of the frozen one-line list comprehension.
    return [number for number in numbers if numbers.count(number) == 1]


def remove_repeated_onto(
    remaining: list[int], original: list[int], suffix: list[int]
) -> list[int]:
    # Direct evaluator for the three frozen verification.k equations.
    if not remaining:
        return suffix
    head, *tail = remaining
    recursive = remove_repeated_onto(tail, original, suffix)
    return [head, *recursive] if original.count(head) == 1 else recursive


examples = [
    [],
    [0],
    [1, 1],
    [1, 2, 1, 3],
    [-1, 0, -1, 2],
    [2, 2, 3, 4, 4, 5],
    [1, 2, 2, 3, 3, 4],
]

print("GROUND SOURCE/SUMMARY COMPARISONS")
for example in examples:
    observed = remove_repeated_onto(example, example, [])
    expected = source_behavior(example)
    print(f"{example!r} -> source={expected!r}, summary={observed!r}")
    assert observed == expected

print()
print("NONEMPTY-SUFFIX RECURRENCE COMPARISONS")
for example, suffix in [
    ([], [9]),
    ([1, 2, 1, 3], [9]),
    ([-1, 0, -1, 2], [7, 8]),
]:
    observed = remove_repeated_onto(example, example, suffix)
    expected = [*source_behavior(example), *suffix]
    print(
        f"input={example!r}, suffix={suffix!r} -> "
        f"expected={expected!r}, summary={observed!r}"
    )
    assert observed == expected

print()
print("COUNTERFACTUAL MUTATION WITNESSES")
witness = [1, 2, 1, 3]
correct = source_behavior(witness)
mutations = {
    "constant-empty": [],
    "identity": witness,
    "retain-duplicates": [
        number for number in witness if witness.count(number) != 1
    ],
    "reverse-survivors": list(reversed(correct)),
}
for name, result in mutations.items():
    print(
        f"{name}: witness={witness!r}, result={result!r}, "
        f"expected={correct!r}, rejected={result != correct}"
    )
    assert result != correct

print("PASS: all ground comparisons agree and all counterfactuals are rejected")
