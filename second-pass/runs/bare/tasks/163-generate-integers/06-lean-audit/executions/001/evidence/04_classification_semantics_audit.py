#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import product


DIGITS = (2, 4, 6, 8)


def operational_model(a: int, b: int) -> list[int]:
    """Independent direct model of the frozen nested-if program."""
    result: list[int] = []
    if a <= b:
        if a <= 2:
            if 2 <= b:
                result = result + [2]
        if a <= 4:
            if 4 <= b:
                result = result + [4]
        if a <= 6:
            if 6 <= b:
                result = result + [6]
        if a <= 8:
            if 8 <= b:
                result = result + [8]
    else:
        if b <= 2:
            if 2 <= a:
                result = result + [2]
        if b <= 4:
            if 4 <= a:
                result = result + [4]
        if b <= 6:
            if 6 <= a:
                result = result + [6]
        if b <= 8:
            if 8 <= a:
                result = result + [8]
    return result


def expected_digit(a: int, b: int, d: int) -> list[int]:
    predicate = (a <= d <= b) or (b <= d <= a)
    return [d] if predicate else []


def definition_model(a: int, b: int) -> list[int]:
    result: list[int] = []
    for digit in DIGITS:
        result += expected_digit(a, b, digit)
    return result


def strict_endpoint_mutation(a: int, b: int) -> list[int]:
    return [d for d in DIGITS if (a < d < b) or (b < d < a)]


def ordered_only_mutation(a: int, b: int) -> list[int]:
    return [d for d in DIGITS if a <= d <= b]


def hard_coded_mutation(_a: int, _b: int) -> list[int]:
    return list(DIGITS)


def reverse_order_mutation(a: int, b: int) -> list[int]:
    return [d for d in reversed(DIGITS) if min(a, b) <= d <= max(a, b)]


wide_domain = range(-5, 21)
positive_domain = range(1, 21)
wide_mismatches = [
    {
        "a": a,
        "b": b,
        "operational": operational_model(a, b),
        "definition": definition_model(a, b),
    }
    for a, b in product(wide_domain, repeat=2)
    if operational_model(a, b) != definition_model(a, b)
]
positive_mismatches = [
    {
        "a": a,
        "b": b,
        "operational": operational_model(a, b),
        "definition": definition_model(a, b),
    }
    for a, b in product(positive_domain, repeat=2)
    if operational_model(a, b) != definition_model(a, b)
]

guard_overlap_count = 0
guard_gap_count = 0
for a, b, d in product(wide_domain, repeat=3):
    positive_guard = (a <= d <= b) or (b <= d <= a)
    negative_guard = not positive_guard
    guard_overlap_count += int(positive_guard and negative_guard)
    guard_gap_count += int(not positive_guard and not negative_guard)

witness_pairs = [
    (2, 8),
    (8, 2),
    (10, 14),
    (3, 7),
    (1, 1),
    (2, 2),
    (8, 8),
    (1, 9),
]
witnesses = [
    {
        "a": a,
        "b": b,
        "operational": operational_model(a, b),
        "definition": definition_model(a, b),
    }
    for a, b in witness_pairs
]

mutations = {
    "strict_endpoint": strict_endpoint_mutation,
    "ordered_only": ordered_only_mutation,
    "hard_coded_full_list": hard_coded_mutation,
    "reverse_order": reverse_order_mutation,
}
mutation_witnesses: dict[str, list[dict[str, object]]] = {}
for name, mutation in mutations.items():
    differences: list[dict[str, object]] = []
    for a, b in product(positive_domain, repeat=2):
        actual = operational_model(a, b)
        mutated = mutation(a, b)
        if actual != mutated:
            differences.append(
                {
                    "a": a,
                    "b": b,
                    "operational": actual,
                    "mutated": mutated,
                }
            )
            if len(differences) == 4:
                break
    mutation_witnesses[name] = differences

classification = [
    {
        "source_rule_id": "rule-b067b43d5f947711d358527708712198f2c109323388e41a86efd408cfe7c3aa",
        "independent_classification": "DEFINITION",
        "reason": (
            "Guarded positive equation for the declared function "
            "expectedDigit; it rewrites no execution construct or cell."
        ),
    },
    {
        "source_rule_id": "rule-098526288db0b9357bcc0dfdb447cbb9838647572e7d85518b225581f438f785",
        "independent_classification": "DEFINITION",
        "reason": (
            "Complementary guarded equation for the declared function "
            "expectedDigit; its guard is the exact Boolean complement of "
            "the first equation."
        ),
    },
    {
        "source_rule_id": "rule-e5fd4b8a680c9837723a78964e7e9f5c5acbab3f9a323002561d8adfacf87cd4",
        "independent_classification": "DEFINITION",
        "reason": (
            "Macro equation for the declared function expected, composing "
            "expectedDigit at 2, 4, 6, and 8 in ascending order."
        ),
    },
]

result = {
    "classification": classification,
    "independent_domain_lemma_count": 0,
    "independent_operational_rule_count": 0,
    "independent_proved_derived_lemma_count": 0,
    "guard_partition": {
        "tested_triples": len(wide_domain) ** 3,
        "overlap_count": guard_overlap_count,
        "gap_count": guard_gap_count,
    },
    "operational_equivalence": {
        "wide_tested_pairs": len(wide_domain) ** 2,
        "wide_mismatch_count": len(wide_mismatches),
        "wide_mismatches": wide_mismatches,
        "positive_tested_pairs": len(positive_domain) ** 2,
        "positive_mismatch_count": len(positive_mismatches),
        "positive_mismatches": positive_mismatches,
    },
    "boundary_and_adversarial_witnesses": witnesses,
    "counterfactual_mutation_witnesses": mutation_witnesses,
}
print(json.dumps(result, indent=2, sort_keys=True))

if guard_overlap_count or guard_gap_count:
    raise SystemExit("expectedDigit guards do not partition the test domain")
if wide_mismatches or positive_mismatches:
    raise SystemExit("definition differs from the frozen operational model")
if any(not differences for differences in mutation_witnesses.values()):
    raise SystemExit("a counterfactual mutation was not detected")
