#!/usr/bin/env python3
# Independent finite sensitivity check used by this audit.
from itertools import combinations


def frozen_source_formula(n: int) -> int:
    zero_count = (n + 1) // 3
    one_count = n - zero_count
    zero_triples = zero_count * (zero_count - 1) * (zero_count - 2) // 6
    one_triples = one_count * (one_count - 1) * (one_count - 2) // 6
    return zero_triples + one_triples


def brute_force_prompt(n: int) -> int:
    values = [i * i - i + 1 for i in range(1, n + 1)]
    return sum(sum(triple) % 3 == 0 for triple in combinations(values, 3))


def summary_formula(n: int) -> int:
    zero_residues = (n + 1) // 3
    return (
        zero_residues * (zero_residues - 1) * (zero_residues - 2) // 6
        + (n - zero_residues)
        * (n - zero_residues - 1)
        * (n - zero_residues - 2)
        // 6
    )


def wrong_zero_count_mutation(n: int) -> int:
    zero_count = n // 3
    one_count = n - zero_count
    return (
        zero_count * (zero_count - 1) * (zero_count - 2) // 6
        + one_count * (one_count - 1) * (one_count - 2) // 6
    )


rows = []
for n in range(1, 61):
    oracle = brute_force_prompt(n)
    source = frozen_source_formula(n)
    summary = summary_formula(n)
    if oracle != source or source != summary:
        rows.append((n, oracle, source, summary))

mutation_witnesses = [
    (n, brute_force_prompt(n), wrong_zero_count_mutation(n))
    for n in range(1, 21)
    if brute_force_prompt(n) != wrong_zero_count_mutation(n)
]

print(f"checked_positive_n=1..60")
print(f"source_vs_bruteforce_mismatches={len(rows)}")
print(f"summary_vs_source_mismatches={len(rows)}")
print(f"boundary_samples={{1:{summary_formula(1)}, 2:{summary_formula(2)}, "
      f"3:{summary_formula(3)}, 5:{summary_formula(5)}, 6:{summary_formula(6)}, "
      f"8:{summary_formula(8)}, 9:{summary_formula(9)}}}")
print(f"wrong_zero_count_first_witness={mutation_witnesses[0]}")
print(f"plus_one_mutation_witness=(5, expected={brute_force_prompt(5)}, "
      f"mutated={summary_formula(5) + 1})")

if rows or not mutation_witnesses:
    raise SystemExit(1)
