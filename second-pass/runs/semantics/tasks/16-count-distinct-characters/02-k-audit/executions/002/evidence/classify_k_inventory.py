#!/usr/bin/env python3
"""Attach theorem-dependence and audit decisions to every inventoried K sentence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


USED_RULES = {
    "reference-semantics/semantics/core.k": {
        131,
        132,
        152,
        158,
        189,
        190,
        191,
        214,
        228,
        229,
    },
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 85},
    "reference-semantics/semantics/call.k": {16, 20, 21, 24, 31, 69},
    "reference-semantics/semantics/methods.k": {
        19,
        113,
        142,
        143,
        155,
        156,
    },
    "reference-semantics/semantics/builtins.k": {21, 25, 41},
    "reference-semantics/semantics/set.k": {
        12,
        13,
        18,
        19,
        20,
        22,
        26,
        27,
    },
}

LOWERCASE_MISMATCH_RULES = {
    ("reference-semantics/semantics/methods.k", line)
    for line in {19, 113, 142, 143, 155, 156}
}

ASCII_LITERAL_BOUNDARY = {
    ("reference-semantics/semantics/str.k", line)
    for line in {14, 15, 16}
}


def classify(record: dict[str, object]) -> tuple[str, str]:
    file = str(record["file"])
    kind = str(record["kind"])
    line = int(record["start_line"])

    if file == "verification.k":
        if kind == "rule":
            return (
                "PROOF_LOCAL_DEFINITIONAL_WRAPPER",
                "Sound: rewrites fresh wrapper syntax to the exact parsed "
                "function term or exact closure body; it displaces no fixed "
                "semantics. Constructor-level KORE equality was checked.",
            )
        return (
            "PROOF_LOCAL_DECLARATION",
            "Fresh wrapper vocabulary only; no function, total, opaque, "
            "priority, or simplification attribute.",
        )

    if (file, line) in LOWERCASE_MISMATCH_RULES:
        return (
            "USED_FIXED_MODEL_MISMATCH",
            "Deterministic and sound in the supplied ASCII case-map model, "
            "but not equivalent to CPython Unicode lower(); witnesses are "
            "'Σσ' (model 2, Python 1) and 'İ' (model 1, Python 2).",
        )

    if line in USED_RULES.get(file, set()):
        return (
            "USED_FIXED_RULE_SOUND_ON_MODELED_VALUES",
            "Reached by the target proof; preserves the exact value/control/"
            "state transition for this program's modeled values. Recursive "
            "functions descend structurally and branch guards are disjoint.",
        )

    if (file, line) in ASCII_LITERAL_BOUNDARY:
        return (
            "FIXED_ASCII_LITERAL_BOUNDARY",
            "Explicit supplied-semantics boundary: concrete string literals "
            "only step when every next character is below 128. The symbolic "
            "claim bypasses literal construction, so this does not repair the "
            "Unicode source-contract gap.",
        )

    if file == "reference-semantics/semantics/concrete.k":
        return (
            "CONCRETE_ONLY_NOT_IN_PROOF_IMPORT_CLOSURE",
            "Defined for MPY-KRUN, not imported by VERIFICATION/MPY; no "
            "positive proof claim can depend on this sentence.",
        )

    if kind == "syntax" and record.get("is_opaque"):
        return (
            "FIXED_OPAQUE_SYMBOL_UNREACHED",
            "Supplied opaque trust boundary, but unreachable from this "
            "program and absent from its postcondition; no target value, "
            "control, state, or termination fact depends on it.",
        )

    if kind == "rule" and record.get("is_priority"):
        return (
            "FIXED_PRIORITY_RULE_UNREACHED",
            "The rule is in supplied semantics but its redex/guard is not "
            "reachable in the target proof; it cannot preempt a target step.",
        )

    if kind == "rule":
        return (
            "FIXED_RULE_UNREACHED",
            "Not reachable from the submitted program/claims. It is part of "
            "the immutable supplied semantics, not a proof-local extension; "
            "no target conclusion depends on it and no false-conclusion "
            "witness is asserted.",
        )

    if kind == "syntax" and record.get("is_total"):
        return (
            "FIXED_TOTAL_DECLARATION_UNREACHED",
            "Supplied total/function declaration not used by the target "
            "unless paired with a separately classified reached rule.",
        )

    return (
        "FIXED_STRUCTURAL_OR_UNUSED_DECLARATION",
        "Module/import/configuration/syntax/context structure from the "
        "immutable supplied semantics; no proof-local logical axiom.",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    decisions = []
    for record in inventory["records"]:
        category, decision = classify(record)
        counts[category] = counts.get(category, 0) + 1
        decisions.append(
            {
                "id": record["id"],
                "kind": record["kind"],
                "attributes": record["attributes"],
                "category": category,
                "decision": decision,
                "normalized_sha256": record["normalized_sha256"],
            }
        )
    document = {
        "schema_version": 1,
        "source_inventory": str(args.inventory),
        "counts": counts,
        "decisions": decisions,
    }
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(counts, sort_keys=True))
    print(f"DECISIONS: {len(decisions)}")
    print("CLASSIFICATION_LEDGER: WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
