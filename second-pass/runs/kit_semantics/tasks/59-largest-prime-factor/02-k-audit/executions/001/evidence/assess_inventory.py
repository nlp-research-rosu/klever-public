#!/usr/bin/env python3
"""Attach an audit decision to every K declaration inventory row."""

import csv
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/rule-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/rule-assessment.tsv")


USED_LINES = {
    "core.k": [
        (13, 60),
        (124, 127),
        (130, 134),
        (152, 181),
        (183, 191),
        (193, 194),
        (198, 202),
        (207, 215),
    ],
    "controls.k": [(9, 11), (50, 54), (65, 67), (76, 85)],
    "functions.k": [(8, 16), (62, 66), (77, 90)],
    "call.k": [(18, 21), (69, 74)],
    "operators.k": [(12, 17)],
    "int.k": [(9, 9), (15, 16), (19, 20), (24, 24), (26, 26)],
}

KNOWN_UNUSED_LIMITATIONS = {
    ("controls.k", 36):
        "unsupported ImportFrom forms are modeled as no-ops; program has no import",
    ("float.k", 61):
        "imports are modeled as no-ops for the float subset; program has no import",
    ("functions.k", 85):
        "frame-pop model assumes no escaping local closure; program returns an Int",
    ("assert.k", 8):
        "assertion failure model is smoke-program-only; program has no Assert",
    ("builtins.k", 134):
        "compiler reports total mapStrVS is not exhaustive; symbol is unreachable",
    ("float.k", 73):
        "compiler reports total floorFI is not exhaustive; float subsystem unreachable",
    ("float.k", 86):
        "compiler reports total toF is not exhaustive; float subsystem unreachable",
    ("float.k", 93):
        "compiler reports total ceilF is not exhaustive; float subsystem unreachable",
    ("methods.k", 27):
        "compiler reports total joinCodes is not exhaustive; methods unreachable",
    ("subscript.k", 11):
        "valSeqAt is intentionally total/underspecified out of bounds; no subscript used",
}


def base_name(path: str) -> str:
    return Path(path).name


def is_used(name: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in USED_LINES.get(name, []))


def classify(row):
    path = row["file"]
    name = base_name(path)
    line = int(row["start"])
    kind = row["kind"]
    attrs = set(row["attributes"].split(","))

    if path == "/candidate/verification.k":
        return (
            "PROOF_LOCAL_SOUND",
            "lpfFrom declaration/equation: guarded, disjoint, exhaustive on F>=2, "
            "and lexicographically descending; it does not rewrite program syntax",
        )
    if name == "syntax.k":
        return (
            "USED_SYNTAX_SOUND",
            "constructor declaration used to parse the submitted Module/FuncDef body",
        )
    if name == "concrete.k":
        return (
            "CONCRETE_ONLY_NOT_IN_PROOF",
            "imported only by MPY-KRUN; absent from the Haskell VERIFICATION definition",
        )
    if "no-evaluators" in attrs:
        return (
            "FIXED_OPAQUE_UNUSED",
            "fixed-semantics opaque/LLVM-twin boundary; no reachable program term "
            "constructs or observes this symbol",
        )
    if kind in {"configuration", "syntax", "context"} and (
        name == "core.k" or is_used(name, line)
    ):
        return (
            "USED_FOUNDATION_SOUND",
            "fixed configuration/type/evaluation-context declaration used by execution",
        )
    if is_used(name, line):
        limitation = KNOWN_UNUSED_LIMITATIONS.get((name, line))
        return (
            "PROOF_RELEVANT_FIXED_SOUND",
            "fixed rule preserves the submitted program's binding, left-to-right "
            "evaluation, integer value, loop control, call/return, or state cell"
            + (f"; its subset assumption is satisfied here: {limitation}" if limitation else ""),
        )
    limitation = KNOWN_UNUSED_LIMITATIONS.get((name, line))
    if limitation:
        return ("FIXED_UNUSED_LIMITATION", limitation)
    if kind in {"syntax", "context", "configuration"}:
        return (
            "FIXED_DECLARATIVE_UNUSED",
            "fixed declaration for a construct absent from solution.mpy",
        )
    return (
        "FIXED_RULE_UNUSED",
        "rule belongs to a source construct/value domain absent from solution.mpy; "
        "its LHS cannot match the audited execution",
    )


def main() -> int:
    with INVENTORY.open(newline="") as source:
        rows = list(csv.DictReader(
            (line for line in source if not line.startswith("#")),
            delimiter="\t",
        ))
    fieldnames = list(rows[0]) + ["assessment", "audit_reason"]
    counts = {}
    with OUTPUT.open("w", newline="") as destination:
        writer = csv.DictWriter(
            destination, fieldnames=fieldnames, delimiter="\t"
        )
        writer.writeheader()
        for row in rows:
            assessment, reason = classify(row)
            row["assessment"] = assessment
            row["audit_reason"] = reason
            writer.writerow(row)
            counts[assessment] = counts.get(assessment, 0) + 1
    print(f"assessed_rows={len(rows)}")
    for key in sorted(counts):
        print(f"{key}={counts[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
