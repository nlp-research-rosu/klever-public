#!/usr/bin/env python3
"""Record the independent semantic classification of every local rule."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
inventory = inventory_verification(workspace)
protected = json.loads(
    Path("/reference/lemma-discovery.json").read_text()
)
protected_by_id = {
    entry["source_rule_id"]: entry for entry in protected["rules"]
}

# These judgments are intentionally stated here rather than inferred from the
# protected manifest.
independent = {
    "rule-91f20c17c57ba9180da217922b572fc0a76ea5b16710c09b18338d1b23b85473": {
        "classification": "OPERATIONAL_RULE",
        "judgment": (
            "Empty-case observation for the added numVals list representation: "
            "#iterNext returns #iterDone. It rewrites the execution cell, is "
            "disjoint from native vCons list iteration, and asserts no "
            "mathematical proposition."
        ),
    },
    "rule-cea43d92c29b50d6a74216af9cad3089b53598c94150b3a31659c6f78faba717": {
        "classification": "OPERATIONAL_RULE",
        "judgment": (
            "Integer-head observation for numVals: it yields the Int head and "
            "the represented tail, exactly mirroring the native vCons iterator "
            "step without changing any non-k cell."
        ),
    },
    "rule-54dd5d736f24ad41b6ad1e0f2f5824f791e6bdd44ac172928408814582982f97": {
        "classification": "OPERATIONAL_RULE",
        "judgment": (
            "Float-head observation for numVals: it yields the Float head and "
            "the represented tail, exactly mirroring the native vCons iterator "
            "step without changing any non-k cell."
        ),
    },
    "rule-e3614434272e9b2b42c9f7e8e025e452ff48db3166ba2b7bfe20ec595fc92069": {
        "classification": "DEFINITION",
        "judgment": (
            "Defining equation for the named total summary oddSquare. Its "
            "positive-and-odd guard and I*I contribution match the source "
            "branch; all other integers contribute zero."
        ),
    },
    "rule-300e691d3915e538e30cb19427da1b148dd7dd25fd7697d8d7f91e05a064417e": {
        "classification": "DEFINITION",
        "judgment": "Base equation of the named doubleDifferenceSpec fold.",
    },
    "rule-9020d9ffb6ad09ba9336e9cd83613d6594f1e8fff41781be8ae89f6830bc24b9": {
        "classification": "DEFINITION",
        "judgment": (
            "Integer recurrence of the named doubleDifferenceSpec fold, adding "
            "the head's oddSquare contribution."
        ),
    },
    "rule-632ca21c26648afb8e00343a60c08cc1e6d5a8d922aaf2065bcc9c1a084dcc35": {
        "classification": "DEFINITION",
        "judgment": (
            "Float recurrence of the named doubleDifferenceSpec fold, ignoring "
            "the non-integer head as the source does."
        ),
    },
    "rule-50c046557451dbdab7f5c046f43f07c21ca92ebcf212aa6ced37c91cef873b8c": {
        "classification": "DEFINITION",
        "judgment": (
            "Base equation for the named loop proof term finalNumber; with no "
            "remaining iteration, the old loop-target value is preserved."
        ),
    },
    "rule-c8650570af342363e786cca6f0bdd9a93077a778a36c65cd34bdca5591b7a384": {
        "classification": "DEFINITION",
        "judgment": (
            "Integer recurrence for the named loop proof term finalNumber, "
            "carrying the current head into the rest of the fold."
        ),
    },
    "rule-f20026069fc0de5560fbc771e2a8e5480a3a42de14d22274694bb6f7c8e3eba2": {
        "classification": "DEFINITION",
        "judgment": (
            "Float recurrence for the named loop proof term finalNumber, "
            "carrying the current head into the rest of the fold."
        ),
    },
}

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
protected_ids = [entry["source_rule_id"] for entry in protected["rules"]]
rows = []
for rule in inventory["rules"]:
    source_rule_id = rule["source_rule_id"]
    judgment = independent[source_rule_id]
    rows.append(
        {
            "source_rule_id": source_rule_id,
            "source_span": [rule["start_line"], rule["end_line"]],
            "normalized_sha256": rule["normalized_sha256"],
            "attributes": rule["attributes"],
            "protected_classification": protected_by_id[source_rule_id][
                "classification"
            ],
            "independent_classification": judgment["classification"],
            "classification_matches": (
                protected_by_id[source_rule_id]["classification"]
                == judgment["classification"]
            ),
            "judgment": judgment["judgment"],
        }
    )

true_domain_ids = [
    source_rule_id
    for source_rule_id, judgment in independent.items()
    if judgment["classification"] == "DOMAIN_LEMMA"
]
simplification_rows = [
    row for row in rows if "simplification" in row["attributes"]
]

result = {
    "verification_module_closure": inventory["verification_modules"],
    "verification_sha256": inventory["verification_sha256"],
    "inventory_sha256": inventory["inventory_sha256"],
    "protected_inventory_sha256": protected["inventory_sha256"],
    "inventory_count": len(inventory_ids),
    "protected_count": len(protected_ids),
    "unique_inventory_ids": len(inventory_ids) == len(set(inventory_ids)),
    "unique_protected_ids": len(protected_ids) == len(set(protected_ids)),
    "exact_ordered_identity_bijection": inventory_ids == protected_ids,
    "all_classifications_match": all(
        row["classification_matches"] for row in rows
    ),
    "simplification_rule_count": len(simplification_rows),
    "simplification_classification_policy_holds": all(
        row["independent_classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
        for row in simplification_rows
    ),
    "true_domain_rule_ids": true_domain_ids,
    "rows": rows,
}
print(json.dumps(result, indent=2, sort_keys=True))
