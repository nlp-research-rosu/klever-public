#!/usr/bin/env python3
"""Audit-owned Stage 3 classification record for 158-find-max."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

# These judgments were reconstructed from verification.k and the supplied MPY
# semantics, not copied from the Stage 3 rationales.
JUDGMENTS = {
    9: (
        "DEFINITION",
        "Base equation of the recursive WordSeq-to-ValSeq encoding.",
    ),
    10: (
        "DEFINITION",
        "Inductive equation of the recursive WordSeq-to-ValSeq encoding.",
    ),
    16: (
        "OPERATIONAL_RULE",
        "Empty-list iterator observation; it is the exact MPY-LIST empty "
        "#iterNext transition after unfolding wordVals.",
    ),
    18: (
        "OPERATIONAL_RULE",
        "Nonempty-list iterator observation; it preserves the continuation "
        "and is the exact MPY-LIST cons #iterNext transition after unfolding "
        "wordVals.",
    ),
    24: (
        "DEFINITION",
        "Macro definition naming the exact translated loop-body AST.",
    ),
    38: (
        "DEFINITION",
        "Macro definition naming the exact translated function-body AST.",
    ),
    51: (
        "DEFINITION",
        "Base equation of the findMaxWords accumulator summary.",
    ),
    54: (
        "DEFINITION",
        "Greater-score branch of the structurally decreasing findMaxWords "
        "recurrence.",
    ),
    61: (
        "DEFINITION",
        "Equal-score/lexicographically-smaller branch of the structurally "
        "decreasing findMaxWords recurrence.",
    ),
    69: (
        "DEFINITION",
        "Smaller-score branch of the structurally decreasing findMaxWords "
        "recurrence.",
    ),
    76: (
        "DEFINITION",
        "Equal-score/not-smaller branch of the structurally decreasing "
        "findMaxWords recurrence.",
    ),
    85: (
        "DEFINITION",
        "First projection equation for the BestState summary.",
    ),
    88: (
        "DEFINITION",
        "Second projection equation for the BestState summary.",
    ),
    92: (
        "DEFINITION",
        "Greater-score recurrence for the bestWord projection; its RHS and "
        "guard are the exact congruence-lift of the findMaxWords equation.",
    ),
    96: (
        "DEFINITION",
        "Greater-score recurrence for the bestScore projection; its RHS and "
        "guard are the exact congruence-lift of the findMaxWords equation.",
    ),
    101: (
        "DEFINITION",
        "Equal-score/smaller recurrence for the bestWord projection; it is "
        "an exact one-step unfolding of the summary.",
    ),
    106: (
        "DEFINITION",
        "Equal-score/smaller recurrence for the bestScore projection; it is "
        "an exact one-step unfolding of the summary.",
    ),
    112: (
        "DEFINITION",
        "Smaller-score recurrence for the bestWord projection; it is an "
        "exact one-step unfolding of the summary.",
    ),
    116: (
        "DEFINITION",
        "Smaller-score recurrence for the bestScore projection; it is an "
        "exact one-step unfolding of the summary.",
    ),
    121: (
        "DEFINITION",
        "Equal-score/not-smaller recurrence for the bestWord projection; it "
        "is an exact one-step unfolding of the summary.",
    ),
    126: (
        "DEFINITION",
        "Equal-score/not-smaller recurrence for the bestScore projection; "
        "it is an exact one-step unfolding of the summary.",
    ),
}


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    stage3_by_id = {
        entry["source_rule_id"]: entry["classification"]
        for entry in discovery["rules"]
    }
    rows = []
    for rule in inventory["rules"]:
        classification, reason = JUDGMENTS[rule["start_line"]]
        rows.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "span": [rule["start_line"], rule["end_line"]],
                "attributes": rule["attributes"],
                "independent_classification": classification,
                "stage3_classification": stage3_by_id[rule["source_rule_id"]],
                "classification_matches": (
                    classification
                    == stage3_by_id[rule["source_rule_id"]]
                ),
                "reason": reason,
            }
        )
    summary = {
        "rule_count": len(rows),
        "all_entries_judged": len(rows) == len(JUDGMENTS),
        "all_stage3_classifications_match": all(
            row["classification_matches"] for row in rows
        ),
        "independent_counts": {
            role: sum(
                row["independent_classification"] == role for row in rows
            )
            for role in (
                "DEFINITION",
                "OPERATIONAL_RULE",
                "PROVED_DERIVED_LEMMA",
                "DOMAIN_LEMMA",
            )
        },
        "simplification_rule_ids": [
            row["source_rule_id"]
            for row in rows
            if "simplification" in row["attributes"]
        ],
        "simplification_roles_valid": all(
            row["independent_classification"]
            in {"DEFINITION", "DOMAIN_LEMMA"}
            for row in rows
            if "simplification" in row["attributes"]
        ),
        "true_domain_rule_ids": [
            row["source_rule_id"]
            for row in rows
            if row["independent_classification"] == "DOMAIN_LEMMA"
        ],
    }
    print(json.dumps({"summary": summary, "rules": rows}, indent=2))


if __name__ == "__main__":
    main()
