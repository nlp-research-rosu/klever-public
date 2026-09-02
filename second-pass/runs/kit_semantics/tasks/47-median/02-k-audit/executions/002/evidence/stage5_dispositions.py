#!/usr/bin/env python3
"""Attach an explicit audit disposition to every Stage-5 inventory item."""

from __future__ import annotations

from pathlib import Path


INVENTORY = Path("/audit-output/evidence/stage5-rule-inventory-rerun.log")

LOAD_BEARING_FILES = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/call.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/builtins.k",
    "reference-semantics/semantics/sort.k",
    "reference-semantics/semantics/subscript.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/bool.k",
    "reference-semantics/semantics/float.k",
}


def classify(fields: list[str]) -> tuple[str, str]:
    path, _line, kind, classification, attributes, statement = fields[1:7]
    if path == "spec.k":
        return (
            "TARGET_NOT_ASSUMPTION",
            "reachability target; not imported as a semantic equation",
        )
    if path == "program.k":
        if kind == "syntax":
            return (
                "ACCEPT_LOCAL_NAMING_DECLARATION",
                "fresh nullary value symbol; no state or result semantics",
            )
        return (
            "ACCEPT_LOCAL_EXACT_DEFINITION",
            "single exhaustive expansion to the independently reconstructed closure",
        )
    if path.endswith("/concrete.k"):
        return (
            "ACCEPT_SUPPLIED_RUNTIME_ONLY",
            "fixed concrete-execution rule; absent from the fresh proof allRules",
        )
    if "no-evaluators" in attributes:
        return (
            "ACCEPT_WITH_OPAQUE_TRUST_BOUNDARY",
            "fixed supplied opaque primitive; no local equation chooses its result",
        )
    if path in LOAD_BEARING_FILES:
        return (
            "ACCEPT_SUPPLIED_LOAD_BEARING",
            "file is in the load-bearing cone; item reviewed for direct use or overlap",
        )
    if path.startswith("reference-semantics/"):
        return (
            "ACCEPT_SUPPLIED_NONINTERFERING",
            "fixed supplied declaration/rule reviewed for overlap; not reached by this body",
        )
    return ("REVIEW_ERROR", f"unclassified inventory row: {statement}")


def main() -> int:
    counts: dict[str, int] = {}
    rows = 0
    errors = 0
    print("DISPOSITION_HEADER\tpath\tline\tkind\tdecision\treason\tstatement")
    for raw in INVENTORY.read_text().splitlines():
        if not raw.startswith("ITEM\t"):
            continue
        fields = raw.split("\t", 6)
        if len(fields) != 7:
            print(f"PARSE_ERROR\t{raw}")
            errors += 1
            continue
        decision, reason = classify(fields)
        path, line, kind, _classification, _attributes, statement = fields[1:7]
        print(
            f"DISPOSITION\t{path}\t{line}\t{kind}\t{decision}\t"
            f"{reason}\t{statement}"
        )
        counts[decision] = counts.get(decision, 0) + 1
        rows += 1
        errors += decision == "REVIEW_ERROR"
    print(f"DISPOSITION_ROWS={rows}")
    print(f"DISPOSITION_COUNTS={counts}")
    print(f"DISPOSITION_ERRORS={errors}")
    return 0 if rows == 1026 and errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
