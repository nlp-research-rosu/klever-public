#!/usr/bin/env python3
"""Finite adversarial checks supporting the independent arithmetic audit."""

from __future__ import annotations


def cube(value: int) -> int:
    return value * value * value


first_antecedents = []
second_antecedents = []
first_counterexamples = []
second_counterexamples = []

for n in range(-3, 31):
    for i in range(-3, 33):
        for d in range(-3, 40):
            common = (
                0 <= i
                and i <= n + 1
                and 0 <= n
                and 0 < d
                and d < cube(n + 1) - cube(n)
            )
            first_guard = common and cube(i) < cube(n) + d
            second_guard = common and cube(i) >= cube(n) + d
            if first_guard:
                first_antecedents.append((n, i, d))
                if not i < n + 1:
                    first_counterexamples.append((n, i, d))
            if second_guard:
                second_antecedents.append((n, i, d))
                if not i == n + 1:
                    second_counterexamples.append((n, i, d))

print(f"first_antecedent_count={len(first_antecedents)}")
print(f"first_witness={first_antecedents[0]}")
print(f"first_counterexamples={first_counterexamples}")
print(f"second_antecedent_count={len(second_antecedents)}")
print(f"second_witness={second_antecedents[0]}")
print(f"second_counterexamples={second_counterexamples}")

# Deliberate false strengthening/off-by-one mutations are rejected by witnesses.
first_mutation_witness = (1, 1, 1)
second_mutation_witness = (1, 2, 1)
print(
    "false_first_mutation_I_lt_N=",
    first_mutation_witness[1] < first_mutation_witness[0],
)
print(
    "false_second_mutation_I_eq_N=",
    second_mutation_witness[1] == second_mutation_witness[0],
)
