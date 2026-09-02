#!/usr/bin/env python3
"""Attach an audit disposition to every row in the exhaustive K inventory."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

SOURCE = Path("/audit-output/evidence/05_static_inventory.tsv")

used_modules = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/call.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/str.k",
    "reference-semantics/semantics/builtins.k",
    "reference-semantics/semantics/subscript.k",
}


def disposition(row: dict[str, str]) -> tuple[str, str]:
    path = row["file"]
    line = int(row["line"])
    if path.startswith("reference-semantics/"):
        relevance = "used-module" if path in used_modules else "unused-module"
        assessment = (
            "Fixed supplied semantics: byte-identical to the trusted mounted tree; "
            "therefore authoritative at the selected semantics level. "
        )
        if relevance == "used-module":
            assessment += (
                "Statically reviewed for the submitted construct path; only a subset "
                "of this module's rows is reached."
            )
        else:
            assessment += "Unreachable from this submitted program and its two claims."
        return relevance, assessment

    if path == "verification.k":
        if line == 10:
            return (
                "proof-local-opaque-symbol",
                "Fresh IntSeq constructor intCodes(Int); result-bearing because it "
                "feeds length, slices, returned strings, and the postcondition.",
            )
        if line == 11:
            return (
                "proof-local-definitional-abstraction",
                "Exact-domain simplification from strToCodes(Int2String(X)) to the "
                "fresh intCodes(X). It loses decimal-code structure but is a "
                "conservative naming equation for the same term; no false fixed-"
                "semantics conclusion witness was found. Its shared use weakens the "
                "formal intent bridge and is tracked as a concern.",
            )
        if line == 14:
            return (
                "proof-local-macro-symbol",
                "Constant macro name for the submitted closure; no independent value.",
            )
        if line == 15:
            return (
                "proof-local-definitional-closure",
                "Expands to the exact regenerated solution.mpy function body and "
                "module parent scope 0; checked mechanically in 04_adequacy.py.",
            )
        if line == 52:
            return (
                "proof-local-spec-function",
                "Postcondition function; result-bearing but does not rewrite Call or "
                "skip the program body.",
            )
        if line == 53:
            return (
                "proof-local-postcondition-equation",
                "Oversize guard SHIFT > LEN; returns a full step-minus-one slice. "
                "Guard is disjoint from and complementary to line 62.",
            )
        if line == 62:
            return (
                "proof-local-postcondition-equation",
                "Normal guard SHIFT <= LEN; suffix(-SHIFT:) plus prefix(:-SHIFT). "
                "Guard is disjoint from and complementary to line 53.",
            )
        return "proof-local-structure", "Module/import structure; no semantic shortcut."

    if path == "spec.k":
        if row["kind"] == "reachability-claim":
            return (
                "target-claim",
                "Result-constraining entry claim over a complete initial call state; "
                "scope and domain are reviewed in stages 4 and 7.",
            )
        return "spec-structure", "Module/import structure."

    return "other", "No separate disposition."


with SOURCE.open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    fieldnames = [*reader.fieldnames, "audit_scope", "assessment"]
    writer = csv.DictWriter(
        sys.stdout, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    for row in reader:
        audit_scope, assessment = disposition(row)
        row["audit_scope"] = audit_scope
        row["assessment"] = assessment
        writer.writerow(row)
