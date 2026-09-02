#!/usr/bin/env python3
"""Independent semantic classification of every reconstructed local rule."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


# These judgments are keyed to independently reconstructed source spans, not
# to the protected manifest's IDs or rationales.
JUDGMENTS = {
    31: ("DEFINITION", "named AST term: exact loop-body statement tree"),
    51: ("DEFINITION", "named AST term: exact post-loop statements and return"),
    61: ("DEFINITION", "named AST term: full source function body"),
    70: ("DEFINITION", "flushSelected defining equation: unequal-count branch"),
    73: ("DEFINITION", "flushSelected defining equation: equal count and empty word"),
    76: ("DEFINITION", "flushSelected defining equation: equal count and nonempty word"),
    81: ("DEFINITION", "selectScan summary composition definition"),
    90: ("DEFINITION", "scanAccum base defining equation"),
    93: ("DEFINITION", "scanAccum recurrence: space and unequal count"),
    98: ("DEFINITION", "scanAccum recurrence: space, equal count, empty word"),
    103: ("DEFINITION", "scanAccum recurrence: space, equal count, nonempty word"),
    115: ("DEFINITION", "scanAccum recurrence: nonspace vowel"),
    123: ("DEFINITION", "scanAccum recurrence: nonspace nonvowel"),
    135: ("DEFINITION", "wordAfter base defining equation"),
    137: ("DEFINITION", "wordAfter recurrence: space resets word"),
    141: ("DEFINITION", "wordAfter recurrence: nonspace extends word"),
    146: ("DEFINITION", "countAfter base defining equation"),
    148: ("DEFINITION", "countAfter recurrence: space resets count"),
    152: ("DEFINITION", "countAfter recurrence: nonspace vowel"),
    158: ("DEFINITION", "countAfter recurrence: nonspace nonvowel"),
    165: ("DEFINITION", "charAfter base defining equation"),
    167: ("DEFINITION", "charAfter recurrence: consume and retain current character"),
}


inventory = inventory_verification(Path("/reference/k-proof"))
protected = json.loads(Path("/reference/lemma-discovery.json").read_text())
protected_by_id = {
    entry["source_rule_id"]: entry for entry in protected["rules"]
}

if {rule["start_line"] for rule in inventory["rules"]} != set(JUDGMENTS):
    raise SystemExit("independent judgment spans do not cover the exact inventory")

rows = []
for index, rule in enumerate(inventory["rules"], 1):
    classification, reason = JUDGMENTS[rule["start_line"]]
    row = {
        "index": index,
        "source_span": f"{rule['start_line']}-{rule['end_line']}",
        "source_rule_id": rule["source_rule_id"],
        "attributes": rule["attributes"],
        "independent_classification": classification,
        "independent_reason": reason,
        "protected_classification": protected_by_id[rule["source_rule_id"]][
            "classification"
        ],
    }
    row["classification_matches"] = (
        row["independent_classification"] == row["protected_classification"]
    )
    row["simplification_policy_ok"] = (
        "simplification" not in rule["attributes"]
        or classification in {"DEFINITION", "DOMAIN_LEMMA"}
    )
    rows.append(row)

summary = {
    "inventory_count": len(rows),
    "independent_counts": {
        name: sum(row["independent_classification"] == name for row in rows)
        for name in (
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        )
    },
    "all_classifications_match": all(
        row["classification_matches"] for row in rows
    ),
    "all_simplification_rules_allowed": all(
        row["simplification_policy_ok"] for row in rows
    ),
    "rows": rows,
}
print(json.dumps(summary, indent=2, sort_keys=True))
if not summary["all_classifications_match"]:
    raise SystemExit(1)
if not summary["all_simplification_rules_allowed"]:
    raise SystemExit(1)
