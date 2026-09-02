#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


independent_roles = [
    {
        "source_rule_id": "rule-7f8c42332f0b798eee0b216c19d5d737994c30bca58bf60acf82eff2cb615db0",
        "classification": "DEFINITION",
        "judgment": "Defines the named factorizeStep AST macro; it states no mathematical proposition and does not preempt execution.",
    },
    {
        "source_rule_id": "rule-ff36487c2202b88e3202d1e6622812de6a27d82188e3b7999b6c7c7be54797e8",
        "classification": "DEFINITION",
        "judgment": "Defines the named factorizeBody AST macro as initialization, the while loop, and return.",
    },
    {
        "source_rule_id": "rule-7520d00b18cd44c15c8c66ee59da1729e0aff44a38220cce83690aca9918b78e",
        "classification": "DEFINITION",
        "judgment": "Defines the named factorizeDef AST macro.",
    },
    {
        "source_rule_id": "rule-974193eeb99c10573f8dab5154f95bf8f6117f8608a552dbe51b0d6bac94b0f2",
        "classification": "DEFINITION",
        "judgment": "Base equation of the factorLoop result/heap recurrence, matching while exit at N <= 1.",
    },
    {
        "source_rule_id": "rule-97414a2f1326ed4caaabdb270b8d32a516ce5379a17fe29c67b89403da76d3e2",
        "classification": "DEFINITION",
        "judgment": "Divisible branch of factorLoop: append D and replace N by the supplied // semantics.",
    },
    {
        "source_rule_id": "rule-fa4a22ace5a93a7480acd4a580108ddb030954fd16f84400b2af42a8ef019e7c",
        "classification": "DEFINITION",
        "judgment": "Nondivisible branch of factorLoop: retain N and increment D.",
    },
    {
        "source_rule_id": "rule-7abb5eb657f4bef944df578672058961f94b444760fa902d543029900e2f1d89",
        "classification": "DEFINITION",
        "judgment": "Names primeFactors as factorLoop initialized with divisor 2 and an empty accumulator.",
    },
    {
        "source_rule_id": "rule-00ba33f1d00d89a1287b827ed0e4d61a72208d9481e855799dfa084cc130eb8a",
        "classification": "DEFINITION",
        "judgment": "Base equation of the final-divisor recurrence.",
    },
    {
        "source_rule_id": "rule-8d7f72419f6087f2e87e0319302781f3a30793025cdfa8d56ddfd4880321eb43",
        "classification": "DEFINITION",
        "judgment": "Divisible branch of the final-divisor recurrence.",
    },
    {
        "source_rule_id": "rule-fb3e8c9a0714f588bbdcc8ba9d5615b6a66551f899d90d882938e80c7e105b1c",
        "classification": "DEFINITION",
        "judgment": "Nondivisible branch of the final-divisor recurrence.",
    },
    {
        "source_rule_id": "rule-7a0b234f2c7d2f2e9f5ca663b20c6f7b0d9cfa7eb71ea38b3a1681cb48235035",
        "classification": "PROVED_DERIVED_LEMMA",
        "judgment": "Exact promoted factorize-loop reachability claim; the base proof excludes this module and the later entry proof imports it.",
    },
]


def source_algorithm(original: int) -> tuple[list[int], int]:
    n = original
    factors: list[int] = []
    divisor = 2
    while n > 1:
        if n % divisor == 0:
            factors.append(divisor)
            n = n // divisor
        else:
            divisor += 1
    return factors, divisor


def summary_recurrences(original: int) -> tuple[list[int], int]:
    n = original
    divisor = 2
    values: list[int] = []
    while True:
        if n <= 1:
            return values, divisor
        py_mod = ((n % divisor) + divisor) % divisor
        if py_mod == 0:
            n = (n - py_mod) // divisor
            values = values + [divisor]
        else:
            divisor = divisor + 1


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


inventory = inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
independent_ids = [entry["source_rule_id"] for entry in independent_roles]
discovery_roles = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
independent_role_map = {
    entry["source_rule_id"]: entry["classification"]
    for entry in independent_roles
}

adversarial_inputs = [1, 2, 3, 4, 8, 25, 49, 70, 97, 360, 499]
adversarial_results = []
for value in adversarial_inputs:
    operational = source_algorithm(value)
    summary = summary_recurrences(value)
    adversarial_results.append(
        {
            "input": value,
            "operational_factors": operational[0],
            "operational_final_divisor": operational[1],
            "summary_factors": summary[0],
            "summary_final_divisor": summary[1],
            "equal": operational == summary,
        }
    )

mismatches: list[dict[str, object]] = []
property_failures: list[dict[str, object]] = []
for value in range(1, 501):
    operational = source_algorithm(value)
    summary = summary_recurrences(value)
    if operational != summary:
        mismatches.append(
            {"input": value, "operational": operational, "summary": summary}
        )
    factors = summary[0]
    if (
        factors != sorted(factors)
        or any(not is_prime(factor) for factor in factors)
        or math.prod(factors) != value
    ):
        property_failures.append({"input": value, "factors": factors})

print(
    json.dumps(
        {
            "independent_classification": independent_roles,
            "inventory_order_equals_independent_order": inventory_ids
            == independent_ids,
            "independent_roles_equal_stage3_roles": independent_role_map
            == discovery_roles,
            "classification_counts": {
                role: list(independent_role_map.values()).count(role)
                for role in (
                    "DEFINITION",
                    "OPERATIONAL_RULE",
                    "PROVED_DERIVED_LEMMA",
                    "DOMAIN_LEMMA",
                )
            },
            "simplification_rules": [
                rule["source_rule_id"]
                for rule in inventory["rules"]
                if "simplification" in rule["attributes"]
            ],
            "operational_correspondence": {
                "formal_input_scope": "N >= 1",
                "exhaustive_finite_scope": "1 <= N <= 500",
                "mismatch_count": len(mismatches),
                "mismatches": mismatches,
                "prime_sorted_product_failure_count": len(property_failures),
                "prime_sorted_product_failures": property_failures,
                "adversarial_results": adversarial_results,
            },
        },
        indent=2,
        sort_keys=True,
    )
)
