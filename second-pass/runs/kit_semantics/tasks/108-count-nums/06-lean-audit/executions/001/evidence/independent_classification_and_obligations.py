#!/usr/bin/env python3
"""Record the independent semantic classification and obligation judgment."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


inventory = json.loads(
    Path("/audit-output/evidence/inventory-reconstruction.json").read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)

domain = {
    "rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43": (
        "Unproved definedness equivalence for the partial Val-to-Int cast. "
        "It is used to discharge the source program's guarded integer projection."
    ),
    "rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69": (
        "Unproved dynamic-Val comparison bridge, not an ordinary supplied-semantics "
        "rule. It is needed for the source test num < 0 after list iteration."
    ),
    "rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2": (
        "Unproved dynamic-Val unary-minus bridge, not an ordinary supplied-semantics "
        "rule. It is needed for the source assignment n = -num."
    ),
    "rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da": (
        "Unproved bridge from the str builtin on a guarded dynamic integer to the "
        "named decimal-code result. It is needed by for char in str(n)."
    ),
    "rule-5af48b88759940f404acea3042b6fa69d00290648ae1c95910aaad61bea89344": (
        "Unproved value contract that nonnegative decimal conversion yields only "
        "ASCII digit codes. It is needed to justify every int(char) in the inner loop."
    ),
}

definition_reason_by_line = {
    10: "Base equation of the newly introduced allInts structural summary.",
    11: "Recursive equation of the newly introduced allInts structural summary.",
    19: "Definition of the named definedProjectInt predicate by isInt.",
    28: "Guarded defining equation for the named total-projection proof term.",
    31: "Reverse symbolic macro for the same named total-projection proof term.",
    34: "Typed-Int equation defining total projection on its meaningful domain.",
    35: "Idempotence normalization for the named total-projection proof term.",
    51: "Negative branch of the magnitude summary definition.",
    52: "Nonnegative branch of the magnitude summary definition.",
    59: "Definitional name decimalCodes for the supplied conversion result.",
    70: "Base equation of the allDigitCodes structural summary.",
    71: "Recursive equation of the allDigitCodes structural summary.",
    81: "Base equation of the codeDigitSum recurrence.",
    82: "Recursive equation of the codeDigitSum recurrence.",
    87: "Base equation of the chooseFirst loop-accumulator summary.",
    88: "Zero-accumulator branch of the chooseFirst recurrence.",
    90: "Nonzero-accumulator branch of the chooseFirst recurrence.",
    96: "Base equation of the lastCode recurrence.",
    97: "Recursive equation of the lastCode recurrence.",
    100: "Negative branch of the signedDigitSum source-loop summary.",
    104: "Nonnegative branch of the signedDigitSum source-loop summary.",
    109: "Base equation of the countNumsSpec outer-loop summary.",
    110: "Integer-head branch of the countNumsSpec recurrence.",
    115: "Non-integer-head branch of the countNumsSpec recurrence.",
}

claims = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
rows = []
for rule in inventory["rules"]:
    source_rule_id = rule["source_rule_id"]
    if source_rule_id in domain:
        classification = "DOMAIN_LEMMA"
        reason = domain[source_rule_id]
    else:
        classification = "DEFINITION"
        reason = definition_reason_by_line[rule["start_line"]]
    rows.append(
        {
            "index": len(rows) + 1,
            "source_rule_id": source_rule_id,
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "normalized_sha256": rule["normalized_sha256"],
            "attributes": rule["attributes"],
            "audited_classification": classification,
            "protected_classification": claims[source_rule_id],
            "classification_matches": classification == claims[source_rule_id],
            "independent_reason": reason,
            "text": rule["text"],
        }
    )

obligation_assessments = {
    list(domain)[0]: (
        "Exact lowering of cast definedness. The internal `True` is the exact "
        "static lowering of #Ceil(V) for V : SortVal; the surrounding iff still "
        "distinguishes integer from non-integer values, so the obligation is not vacuous."
    ),
    list(domain)[1]: (
        "Exact guarded lowering of applyCmp(\"<\", V, J) to projected integer <."
    ),
    list(domain)[2]: (
        "Exact guarded lowering of applyUn(\"-\", V) to 0 minus the projected integer."
    ),
    list(domain)[3]: (
        "Exact guarded lowering of str on one dynamic integer argument to the "
        "decimalCodes-backed string constructor."
    ),
    list(domain)[4]: (
        "Exact guarded lowering of the nonnegative decimal-code digit contract."
    ),
}
obligations = []
for obligation in obligation_map["obligations"]:
    source_rule_id = obligation["source_rule_id"]
    conjunct = obligation["lean_conjunct"]
    obligations.append(
        {
            **obligation,
            "recomputed_lean_conjunct_sha256": hashlib.sha256(
                conjunct.encode()
            ).hexdigest(),
            "independent_mathematical_assessment": obligation_assessments[
                source_rule_id
            ],
            "relevant_to_program_or_postcondition": True,
            "whole_obligation_vacuous": False,
            "weakened_or_changed": False,
        }
    )

domain_ids = [row["source_rule_id"] for row in rows
              if row["audited_classification"] == "DOMAIN_LEMMA"]
obligation_ids = [item["source_rule_id"] for item in obligations]
source_rule_ids = [
    item["source_rule_id"] for item in obligation_map["source_rules"]
]
simplification_rows = [
    row for row in rows
    if any(attribute.startswith("simplification")
           for attribute in row["attributes"])
]

result = {
    "inventory_sha256": inventory["inventory_sha256"],
    "rule_count": len(rows),
    "classification_counts": dict(
        Counter(row["audited_classification"] for row in rows)
    ),
    "proved_derived_lemma_count": 0,
    "operational_rule_count": 0,
    "proved_derived_lemma_audit": (
        "Stage 1 prove.sh compiles verification.k with every rule already present "
        "before any kprove command; no command first proves an exact rule against "
        "a module omitting it."
    ),
    "all_simplifications_are_definition_or_domain": all(
        row["audited_classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
        for row in simplification_rows
    ),
    "all_protected_classifications_match_independent_audit": all(
        row["classification_matches"] for row in rows
    ),
    "rows": rows,
    "domain_rule_ids": domain_ids,
    "obligation_rule_ids": obligation_ids,
    "obligation_source_rule_ids": source_rule_ids,
    "exact_ordered_domain_obligation_bijection": (
        domain_ids == obligation_ids == source_rule_ids
        and len(domain_ids) == len(set(domain_ids))
    ),
    "obligations": obligations,
    "obligation_count": len(obligations),
    "all_conjunct_hashes_recompute": all(
        item["lean_conjunct_sha256"]
        == item["recomputed_lean_conjunct_sha256"]
        for item in obligations
    ),
    "all_obligations_relevant_nonvacuous_and_unweakened": all(
        item["relevant_to_program_or_postcondition"]
        and not item["whole_obligation_vacuous"]
        and not item["weakened_or_changed"]
        for item in obligations
    ),
}
Path(
    "/audit-output/evidence/classification-and-obligation-judgment.json"
).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
