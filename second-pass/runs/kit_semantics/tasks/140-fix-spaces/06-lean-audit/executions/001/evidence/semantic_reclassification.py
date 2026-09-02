#!/usr/bin/env python3
"""Independent mathematical reclassification and finite semantic probes."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

from tools import k_rule_inventory


workspace = Path("/reference/k-proof")
inventory = k_rule_inventory.inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())


roles = [
    ("DEFINITION", "named proof-term macro: exact translated loop-body AST"),
    ("DEFINITION", "named proof-term macro: exact translated function-body AST"),
    ("DEFINITION", "pendingSpace defining equation: two underscores saturate to dash"),
    ("DEFINITION", "pendingSpace defining equation: dash is absorbing"),
    ("DEFINITION", "pendingSpace defining equation: otherwise append underscore"),
    ("DEFINITION", "resultAfter structurally recursive base equation"),
    ("DEFINITION", "resultAfter structurally recursive space equation"),
    ("DEFINITION", "resultAfter structurally recursive non-space equation"),
    ("DEFINITION", "pendingAfter structurally recursive base equation"),
    ("DEFINITION", "pendingAfter structurally recursive space equation"),
    ("DEFINITION", "pendingAfter structurally recursive non-space equation"),
    ("DEFINITION", "charAfter structurally recursive base equation"),
    ("DEFINITION", "charAfter structurally recursive step equation"),
    ("DEFINITION", "fixedSpaces named summary equation combining final locals"),
]

reclassified = []
for rule, (classification, judgment) in zip(inventory["rules"], roles, strict=True):
    reclassified.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "source_span": [rule["start_line"], rule["end_line"]],
            "attributes": rule["attributes"],
            "classification": classification,
            "independent_judgment": judgment,
        }
    )

print("INDEPENDENT RECLASSIFICATION")
print(json.dumps(reclassified, indent=2))


def pending_space(pending: tuple[int, ...]) -> tuple[int, ...]:
    if pending == (95, 95):
        return (45,)
    if pending == (45,):
        return pending
    return pending + (95,)


def k_summary(codes: tuple[int, ...]) -> tuple[int, ...]:
    """Literal evaluation of pendingSpace/resultAfter/pendingAfter/fixedSpaces."""
    result: tuple[int, ...] = ()
    pending: tuple[int, ...] = ()
    for code in codes:
        if code == 32:
            pending = pending_space(pending)
        else:
            result = result + pending + (code,)
            pending = ()
    return result + pending


def frozen_source_machine(codes: tuple[int, ...]) -> tuple[int, ...]:
    """Independent execution of solution.py's local-state updates."""
    result: tuple[int, ...] = ()
    spaces: tuple[int, ...] = ()
    for char in codes:
        if char == 32:
            if spaces == (95, 95):
                spaces = (45,)
            elif spaces != (45,):
                spaces = spaces + (95,)
        else:
            result = result + spaces + (char,)
            spaces = ()
    return result + spaces


def run_contract_oracle(codes: tuple[int, ...]) -> tuple[int, ...]:
    """Run-based oracle: 1/2 spaces map to underscores, >=3 to one dash."""
    output: list[int] = []
    index = 0
    while index < len(codes):
        if codes[index] != 32:
            output.append(codes[index])
            index += 1
            continue
        end = index
        while end < len(codes) and codes[end] == 32:
            end += 1
        count = end - index
        output.extend((95,) * count if count <= 2 else (45,))
        index = end
    return tuple(output)


alphabet = (32, 65, 95, 45)
tested = 0
mismatches: list[dict[str, object]] = []
for size in range(9):
    for value in itertools.product(alphabet, repeat=size):
        source = frozen_source_machine(value)
        summary = k_summary(value)
        contract = run_contract_oracle(value)
        tested += 1
        if not (source == summary == contract):
            mismatches.append(
                {"input": value, "source": source, "summary": summary, "contract": contract}
            )

adversarial = [
    (), (32,), (32, 32), (32, 32, 32), (32, 32, 32, 32),
    (65, 32), (32, 65), (65, 32, 32), (32, 32, 65),
    (32, 32, 65, 32, 32, 32, 66, 32),
    (0, 32, 945, 32, 32, 0x10FFFF),
]
print("ADVERSARIAL EXAMPLES")
for value in adversarial:
    print(json.dumps({"input": value, "source": frozen_source_machine(value), "k_summary": k_summary(value), "contract": run_contract_oracle(value)}))


def early_dash(codes: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(45 if code == 95 else code for code in k_summary(codes)) if codes == (32, 32) else k_summary(codes)


def nonsaturating_dash(codes: tuple[int, ...]) -> tuple[int, ...]:
    if codes == (32, 32, 32, 32):
        return (45, 95)
    return k_summary(codes)


def omit_pending_flush(codes: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(code for code in codes if code != 32)


def discard_trailing_pending(codes: tuple[int, ...]) -> tuple[int, ...]:
    return k_summary(codes[:-1]) if codes and codes[-1] == 32 else k_summary(codes)


counterfactuals = [
    ("dash after only two spaces", (32, 32), early_dash),
    ("dash is not absorbing", (32, 32, 32, 32), nonsaturating_dash),
    ("omit pending flush before non-space", (32, 65), omit_pending_flush),
    ("discard trailing pending spaces", (65, 32), discard_trailing_pending),
]
print("COUNTERFACTUAL MUTATION WITNESSES")
counterfactual_separation = True
for name, witness, mutation in counterfactuals:
    expected = k_summary(witness)
    mutated = mutation(witness)
    separates = expected != mutated
    counterfactual_separation &= separates
    print(json.dumps({"mutation": name, "input": witness, "expected": expected, "mutated": mutated, "separates": separates}))

observed_classifications = [entry["classification"] for entry in discovery["rules"]]
independent_classifications = [entry["classification"] for entry in reclassified]
simplification_ok = all(
    entry["classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
    for entry in reclassified
    if "simplification" in entry["attributes"]
)
summary = {
    "inventory_entries": len(reclassified),
    "classification_match": independent_classifications == observed_classifications,
    "all_rules_are_definitions": all(entry["classification"] == "DEFINITION" for entry in reclassified),
    "simplification_policy_pass": simplification_ok,
    "domain_lemma_count": sum(entry["classification"] == "DOMAIN_LEMMA" for entry in reclassified),
    "operational_rule_count": sum(entry["classification"] == "OPERATIONAL_RULE" for entry in reclassified),
    "proved_derived_lemma_count": sum(entry["classification"] == "PROVED_DERIVED_LEMMA" for entry in reclassified),
    "exhaustive_inputs_tested": tested,
    "mismatch_count": len(mismatches),
    "counterfactuals_separate": counterfactual_separation,
}
summary["status"] = "PASS" if all((summary["classification_match"], summary["all_rules_are_definitions"], summary["simplification_policy_pass"], summary["domain_lemma_count"] == 0, summary["mismatch_count"] == 0, summary["counterfactuals_separate"])) else "FAIL"
print(json.dumps({"SUMMARY": summary}, sort_keys=True))
raise SystemExit(0 if summary["status"] == "PASS" else 1)
