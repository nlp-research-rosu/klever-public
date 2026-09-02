#!/usr/bin/env python3
"""Attach the review's per-entry disposition to the exhaustive K inventory."""

from __future__ import annotations

import csv
from pathlib import Path


source = Path("/audit-output/evidence/rule_inventory.tsv")
target = Path("/audit-output/evidence/rule_assessment.tsv")
rows = list(csv.DictReader(source.open(), dialect="excel-tab"))


def disposition(row):
    file = row["file"]
    line = int(row["line"])
    kind = row["kind"]
    attrs = row["attributes"]

    if file == "verification.k":
        if line in {7, 8, 17, 18, 21, 22, 45, 46, 49, 51, 52, 53, 1, 3, 4}:
            return (
                "ACCEPTED-EXACT-PINNING",
                "Exact constructor definitions, inert runner expansion, or module plumbing; "
                "mechanical comparison and body mutation confirm execution dependence.",
            )
        if line in {26, 27, 29, 30}:
            return (
                "DOMAIN-NARROWING-UNUSED",
                "Defines 'letter' as ASCII mapSwap change; false as a Python-Unicode "
                "characterization (for example U+4E2D), though these helpers are unused by the claims.",
            )
        if line in {37, 41}:
            return (
                "TRUE-LOOKING-UNVALIDATED-BRIDGE",
                "Result-bearing simplification used by the reverse claim. No false witness "
                "was found, but bridge-free universal connection claims did not close.",
            )

    if file == "spec.k" and kind == "claim":
        return (
            "CLOSES-BUT-INADQUATE",
            "Freshly closes and constrains a result, but its ASCII mapSwap partition/result "
            "does not cover the unrestricted Python string contract.",
        )

    if file.startswith("reference-semantics/"):
        if file.endswith("semantics/str.k") and line in {13, 14, 15, 16}:
            return (
                "FIXED-MODEL-LIMITATION",
                "Supplied concrete literal bridge is explicitly ASCII-only; a Unicode literal "
                "fails concrete execution before the program runs.",
            )
        if file.endswith("semantics/methods.k") and (
            line in {15, 21, 118, 119, 149, 150, 151, 152, 162, 163, 164}
        ):
            return (
                "FIXED-MODEL-LIMITATION",
                "Equations are coherent for the supplied ASCII code model but do not implement "
                "Python Unicode isalpha/swapcase on the source-contract domain.",
            )
        if "no-evaluators" in attrs:
            return (
                "ACCEPTED-INERT-OPAQUE",
                "Fixed supplied opaque primitive; unreachable from this solution term and "
                "therefore cannot affect its control, state, or result.",
            )
        return (
            "ACCEPTED-FIXED",
            "Reviewed as part of the immutable supplied definition. It is coherent on its "
            "declared subset or unreachable from this program; no proof-local false conclusion "
            "witness was found beyond the separately marked string-model limitations.",
        )

    return (
        "ACCEPTED-PLUMBING",
        "Module, import, syntax, or claim plumbing with no independent result-bearing axiom.",
    )


fieldnames = list(rows[0]) + ["disposition", "review_rationale"]
with target.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=fieldnames, dialect="excel-tab")
    writer.writeheader()
    for row in rows:
        row["disposition"], row["review_rationale"] = disposition(row)
        writer.writerow(row)

counts = {}
for row in rows:
    key = disposition(row)[0]
    counts[key] = counts.get(key, 0) + 1
print(f"assessed_rows={len(rows)}")
for key, count in sorted(counts.items()):
    print(f"{key}\t{count}")
