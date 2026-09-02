#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


independent = {
    "rule-bb601208edb1e96080955b1328dafddf878fccfb2dce6832f739299c2b3238de": (
        "DEFINITION",
        "Nullary named proof term expanding to the exact loop-condition AST.",
    ),
    "rule-211588c9e5b79676333afd044a4f025ce5a926e434e042c16ba8ff965176dff5": (
        "DEFINITION",
        "Nullary named proof term expanding to the exact translated loop-body AST.",
    ),
    "rule-72490e5f66a388ba81e28c7d33d85162be231d30fbfc42ada45ce48e94f1b47a": (
        "DEFINITION",
        "Nullary constructor macro naming the closed translated source program.",
    ),
    "rule-1b6dfc30f83e14335a83a1746f3105c6dee0842578ac512515f9f976bcf8c44d": (
        "OPERATIONAL_RULE",
        "Ordinary observation rewrite recognizing structural identity of two programs.",
    ),
    "rule-5d78af83c186109d1745d13d0f1814d6752c84c8c9c47e209a5c7dcadafd402f": (
        "DEFINITION",
        "Even-digit branch of the addOddDigit summary definition.",
    ),
    "rule-437c4b2500798a57406f8d142559444c31e2437b03b5fe055671c6b689e3540e": (
        "DEFINITION",
        "First-odd-digit branch of the addOddDigit summary definition.",
    ),
    "rule-89daad84beeed92afb1ee55504d822d521105908ea9806147e9d9e3147290ec9": (
        "DEFINITION",
        "Subsequent-odd-digit branch of the addOddDigit summary definition.",
    ),
    "rule-e11ad215fdd840b01bcd1242471ce6eec8653123658ff8b63379ca602d63489b": (
        "DEFINITION",
        "Base equation of the oddProductFrom digit-fold recurrence.",
    ),
    "rule-6f05f0cf15dc24aba0468572926489fbee6552fbb026dbafa4cc55d063dd2200": (
        "DEFINITION",
        "Recursive equation consuming one positive base-10 digit.",
    ),
    "rule-ac1c567b0b62d1c41908cf0eddc4e86fd1188c897da6982587d3b155b82122df": (
        "DEFINITION",
        "Wrapper definition initializing the digit fold with the zero sentinel.",
    ),
    "rule-c69abfdd9a91259eebdc62439ad213ee855f4b5c17687e0e4e0d421e2057e987": (
        "DEFINITION",
        "Base equation of the finalScratchDigit recurrence.",
    ),
    "rule-bd4d10518278875bfc2e732411dd8f7adf6cfa7803bd88a85b0e94d0afaeab06": (
        "DEFINITION",
        "Recursive equation tracking the digit written by each loop iteration.",
    ),
}

inventory = inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
claimed = {
    item["source_rule_id"]: item["classification"]
    for item in discovery["rules"]
}
inventory_ids = [item["source_rule_id"] for item in inventory["rules"]]

assert list(independent) == inventory_ids
assert set(independent) == set(claimed)
assert all(independent[rule_id][0] == claimed[rule_id] for rule_id in inventory_ids)
assert all(
    not (
        "simplification" in rule["attributes"]
        and independent[rule["source_rule_id"]][0]
        not in {"DEFINITION", "DOMAIN_LEMMA"}
    )
    for rule in inventory["rules"]
)


def add_odd_digit(accumulator: int, digit: int) -> int:
    if digit % 2 == 0:
        return accumulator
    if accumulator == 0:
        return digit
    return accumulator * digit


def summary_loop(number: int, accumulator: int, scratch: int) -> tuple[int, int]:
    while number > 0:
        scratch = number % 10
        accumulator = add_odd_digit(accumulator, scratch)
        number //= 10
    return accumulator, scratch


def source_loop(number: int, accumulator: int, scratch: int) -> tuple[int, int]:
    while number > 0:
        scratch = number % 10
        if scratch % 2 == 1:
            if accumulator == 0:
                accumulator = scratch
            else:
                accumulator = accumulator * scratch
        number = number // 10
    return accumulator, scratch


mismatches = []
tested_cases = 0
for number in range(0, 10001):
    for accumulator in (-3, 0, 1, 2, 5):
        for scratch in (-7, 0, 9):
            tested_cases += 1
            if source_loop(number, accumulator, scratch) != summary_loop(
                number, accumulator, scratch
            ):
                mismatches.append((number, accumulator, scratch))

representatives = {
    number: {
        "source_result_and_final_scratch": source_loop(number, 0, 0),
        "summary_result_and_final_scratch": summary_loop(number, 0, 0),
    }
    for number in (1, 4, 10, 101, 235, 2468, 10203, 13579, 999999)
}

counterfactuals = {
    "constant_zero_fails_at_1": summary_loop(1, 0, 0)[0] != 0,
    "identity_fails_at_235": summary_loop(235, 0, 0)[0] != 235,
    "constant_one_fails_at_4": summary_loop(4, 0, 0)[0] != 1,
    "final_scratch_identity_fails_at_235": summary_loop(235, 0, 0)[1] != 235,
}
assert not mismatches
assert all(counterfactuals.values())

print(
    json.dumps(
        {
            "independent_classifications": [
                {
                    "source_rule_id": rule_id,
                    "classification": independent[rule_id][0],
                    "semantic_basis": independent[rule_id][1],
                    "stage3_match": independent[rule_id][0] == claimed[rule_id],
                }
                for rule_id in inventory_ids
            ],
            "simplification_rule_count": sum(
                "simplification" in rule["attributes"]
                for rule in inventory["rules"]
            ),
            "true_domain_lemma_ids": [
                rule_id
                for rule_id in inventory_ids
                if independent[rule_id][0] == "DOMAIN_LEMMA"
            ],
            "true_proved_derived_lemma_ids": [
                rule_id
                for rule_id in inventory_ids
                if independent[rule_id][0] == "PROVED_DERIVED_LEMMA"
            ],
            "operational_alignment_tested_cases": tested_cases,
            "operational_alignment_mismatches": mismatches,
            "representative_witnesses": representatives,
            "counterfactual_witnesses": counterfactuals,
        },
        indent=2,
        sort_keys=True,
    )
)
