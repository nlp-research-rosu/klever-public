#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventoried K sentence."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


PROOF_RULE_DECISIONS = {
    14: (
        "UNSOUND_OPERATIONAL_BRIDGE",
        "Preempts fixed replace/float execution and has no bridge-free value or "
        "binding connection theorem.",
    ),
    19: (
        "UNSOUND_RESULT_ORACLE",
        "Produces equation-free commaDecimal; the value influences equality, "
        "ordering, return, and the postcondition.",
    ),
    26: (
        "UNSOUND_RESULT_ORACLE",
        "Replaces fixed Float equality with equation-free sameFloat and has no "
        "connection theorem.",
    ),
    35: (
        "SOUND_ENTRY_DEFINITION",
        "Mechanical constructor comparison pins the exact submitted body.",
    ),
    61: ("SOUND_DEFINITION", "Identity on Int."),
    62: ("SOUND_DEFINITION", "Identity on Float."),
    63: (
        "FORMAL_DEFINITION_DEPENDS_ON_REJECTED_ORACLE",
        "Names commaDecimal but does not establish decimal parsing.",
    ),
    66: ("SOUND_DEFINITION", "Uses built-in integer equality."),
    67: (
        "CONDITIONAL_FIXED_PRIMITIVE",
        "Uses supplied-semantics intToF and eqF trust boundary.",
    ),
    68: (
        "CONDITIONAL_FIXED_PRIMITIVE",
        "Uses supplied-semantics intToF and eqF trust boundary.",
    ),
    69: (
        "FORMAL_DEFINITION_DEPENDS_ON_REJECTED_ORACLE",
        "Reuses sameFloat; it does not independently define numeric equality.",
    ),
    74: (
        "FORMAL_DEFINITION_BUT_CIRCULAR_POSTCONDITION",
        "Structurally chooses a result using the same result-bearing oracles as "
        "execution; it is not an independent numeric contract.",
    ),
}

PROOF_SYNTAX_DECISIONS = {
    11: (
        "REJECT_RESULT_BEARING_OPAQUE_SYMBOL",
        "commaDecimal is total/no-evaluators but has no equations or connection theorem.",
    ),
    13: ("SOUND_CONTROL_MARKER", "Internal continuation marker only."),
    24: (
        "REJECT_RESULT_BEARING_OPAQUE_SYMBOL",
        "sameFloat is total/no-evaluators but has no equations or connection theorem.",
    ),
    34: ("SOUND_ENTRY_SYMBOL", "Entry constructor expanded by the exact-body rule."),
    60: ("SOUND_FORMAL_SUMMARY_SYMBOL", "Coverage supplied by three sort cases."),
    65: ("SOUND_FORMAL_SUMMARY_SYMBOL", "Coverage supplied by four sort-pair cases."),
    73: (
        "SOUND_FORMAL_SYMBOL_BUT_INADEQUATE_PROPERTY",
        "Function is defined, but its meaning depends on circular result oracles.",
    ),
}


def main() -> None:
    inventory_path = Path("/audit-output/evidence/05-rule-inventory.json")
    document = json.loads(inventory_path.read_text())
    assessed = []
    for record in document["records"]:
        item = dict(record)
        source_class = item["source_class"]
        keyword = item["keyword"]
        line = item["start_line"]
        if source_class == "supplied-semantics":
            decision = "ACCEPTED_FIXED_SUPPLIED_SEMANTICS"
            reason = (
                "Immutable byte-identical SUPPLIED_SEMANTICS baseline; candidate "
                "did not add or alter this sentence. Program-relevant rules and "
                "opaque primitive dependencies are separately mapped in REVIEW.md."
            )
        elif source_class == "target-spec" and keyword == "claim":
            decision = "CLOSES_BUT_NOT_LEGIT"
            reason = (
                "Depends on rejected proof-local operational/result oracles and "
                "uses expectedCompare rather than an independently connected contract."
            )
        elif source_class == "proof-local" and keyword == "rule":
            decision, reason = PROOF_RULE_DECISIONS[line]
        elif source_class == "proof-local" and keyword == "syntax":
            decision, reason = PROOF_SYNTAX_DECISIONS[line]
        else:
            decision = "STRUCTURAL_SENTENCE"
            reason = "Module/import boundary; no independent semantic equation."
        item["audit_decision"] = decision
        item["audit_reason"] = reason
        assessed.append(item)

    relevant = [
        item
        for item in assessed
        if item["keyword"] in {"syntax", "rule", "claim", "context", "configuration"}
    ]
    if len(relevant) != (
        227 + 695 + 5 + 1 + 7 + 12 + 9
    ):
        raise AssertionError(f"unexpected assessed sentence count: {len(relevant)}")
    counts = Counter(item["audit_decision"] for item in relevant)
    output_document = {
        "schema_version": 1,
        "inventory_sha256": hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
        "relevant_sentence_count": len(relevant),
        "decision_counts": dict(sorted(counts.items())),
        "records": assessed,
    }
    encoded = json.dumps(output_document, indent=2, sort_keys=True) + "\n"
    output = Path("/audit-output/evidence/05-rule-assessment.json")
    output.write_text(encoded)
    print(f"RELEVANT_SENTENCES_ASSESSED: {len(relevant)}")
    print(f"DECISION_COUNTS: {dict(sorted(counts.items()))}")
    print(f"ASSESSMENT_SHA256: {hashlib.sha256(encoded.encode()).hexdigest()}")
    print(f"OUTPUT: {output}")


if __name__ == "__main__":
    main()
