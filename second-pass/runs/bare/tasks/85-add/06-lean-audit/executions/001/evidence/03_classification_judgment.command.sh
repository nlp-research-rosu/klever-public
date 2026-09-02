#!/usr/bin/env bash
set -euxo pipefail
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
PYTHONPATH=/reference python3 - <<'PY'
import itertools
import json
from pathlib import Path
from tools import k_rule_inventory

workspace = Path("/reference/k-proof")
inventory = k_rule_inventory.inventory_verification(workspace)
protected = json.loads(Path("/reference/lemma-discovery.json").read_text())

by_id = {
    entry["source_rule_id"]: entry
    for entry in inventory["rules"]
}
classification_rows = []
for protected_entry in protected["rules"]:
    rule = by_id[protected_entry["source_rule_id"]]
    text = rule["text"]
    if text.lstrip().startswith("rule oddIndexEvenSum("):
        independent_classification = "DEFINITION"
        role = "base equation or structural recurrence for the named mathematical summary oddIndexEvenSum"
    elif text.lstrip().startswith("rule solutionProgram =>"):
        independent_classification = "DEFINITION"
        role = "macro expansion for the named proof term solutionProgram"
    else:
        independent_classification = "UNACCOUNTED"
        role = "no recognized definitional or operational role"
    classification_rows.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "source_span": [rule["start_line"], rule["end_line"]],
            "attributes": rule["attributes"],
            "protected_classification": protected_entry["classification"],
            "independent_classification": independent_classification,
            "role": role,
            "classification_match": (
                protected_entry["classification"]
                == independent_classification
            ),
        }
    )

macro_rule = inventory["rules"][3]["text"]
macro_rhs = macro_rule.split("=>", 1)[1]
solution_mpy = (workspace / "solution.mpy").read_text()
macro_exact_ignoring_layout = (
    "".join(macro_rhs.split()) == "".join(solution_mpy.split())
)

def even_part(value):
    return value if value % 2 == 0 else 0

def frozen_summary(values):
    if len(values) < 2:
        return 0
    return even_part(values[1]) + frozen_summary(values[2:])

def contract_oracle(values):
    return sum(
        value
        for index, value in enumerate(values)
        if index % 2 == 1 and value % 2 == 0
    )

def counterfactual_even_indices(values):
    return sum(
        value
        for index, value in enumerate(values)
        if index % 2 == 0 and value % 2 == 0
    )

tested = 0
mismatches = []
counterfactual_witnesses = []
alphabet = (-3, -2, -1, 0, 1, 2, 3)
for length in range(0, 7):
    for values in itertools.product(alphabet, repeat=length):
        tested += 1
        observed = frozen_summary(values)
        expected = contract_oracle(values)
        if observed != expected:
            mismatches.append([values, observed, expected])
        wrong = counterfactual_even_indices(values)
        if wrong != expected and len(counterfactual_witnesses) < 5:
            counterfactual_witnesses.append(
                [values, wrong, expected]
            )

result = {
    "classification_rows": classification_rows,
    "all_independent_classifications_match": all(
        row["classification_match"] for row in classification_rows
    ),
    "simplification_rule_ids": [
        rule["source_rule_id"]
        for rule in inventory["rules"]
        if "simplification" in rule["attributes"]
    ],
    "independent_domain_rule_ids": [],
    "protected_domain_rule_ids": [
        entry["source_rule_id"]
        for entry in protected["rules"]
        if entry["classification"] == "DOMAIN_LEMMA"
    ],
    "solution_program_macro_matches_solution_mpy_ignoring_layout": (
        macro_exact_ignoring_layout
    ),
    "summary_contract_exhaustive_sample_count": tested,
    "summary_contract_mismatch_count": len(mismatches),
    "summary_contract_first_mismatches": mismatches[:5],
    "counterfactual_even_index_witnesses": counterfactual_witnesses,
}
print(json.dumps(result, indent=2, sort_keys=True))
assert result["all_independent_classifications_match"]
assert not result["simplification_rule_ids"]
assert not result["independent_domain_rule_ids"]
assert not result["protected_domain_rule_ids"]
assert macro_exact_ignoring_layout
assert not mismatches
assert counterfactual_witnesses
PY
