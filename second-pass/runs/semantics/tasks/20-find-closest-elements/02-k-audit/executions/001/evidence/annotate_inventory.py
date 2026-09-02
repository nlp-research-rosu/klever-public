#!/usr/bin/env python3
"""Attach an audit decision to every row of k_inventory.tsv."""

from __future__ import annotations

import csv
from pathlib import Path


SOURCE = Path("/audit-output/evidence/k_inventory.tsv")
OUTPUT = Path("/audit-output/evidence/k_inventory_review.tsv")


USED_BASELINE_FILES = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/call.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/float.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/subscript.k",
    "reference-semantics/semantics/tuple.k",
    "reference-semantics/semantics/str.k",
    "reference-semantics/semantics/builtins.k",
}


def verification_assessment(line: int) -> tuple[str, str]:
    if line in {7, 8, 13, 14}:
        return (
            "ACCEPT_EXACT_AST_FRAGMENT",
            "Macro declaration/equation text matches the translated loop condition or body.",
        )
    if line in {39, 40}:
        return (
            "PINNING_GAP_MANUAL_COPY",
            "Manual body equation matches the submitted AST by review, but the proof never loads solution.mpy.",
        )
    if 58 <= line <= 71:
        return (
            "ACCEPT_STRUCTURAL_DEFINITION",
            "Constructor conversion/length equations are exhaustive, disjoint, and descending.",
        )
    if line == 72:
        return (
            "LIMITED_TOTAL_ABSTRACTION",
            "Declared total beyond its equations; .FloatSeq/negative/OOB terms remain abstract. Target uses in-bounds indices.",
        )
    if line in {73, 74, 80}:
        return (
            "ACCEPT_ON_GUARDED_DOMAIN",
            "Accessor equation is mathematically correct on its explicit in-bounds/descent domain.",
        )
    if 87 <= line <= 116:
        return (
            "ACCEPT_PAIR_DEFINITION",
            "Projection, ordering, and strict-improvement equations match the program's pair update.",
        )
    if line == 124:
        return (
            "LIMITED_TOTAL_ABSTRACTION",
            "scanPairs is totalized over arbitrary indices although only 0<=I<J<len is operationally justified.",
        )
    if 126 <= line <= 141:
        return (
            "ACCEPT_ON_LOOP_INDEX_INVARIANT",
            "Equations enumerate lexicographic pairs and descend only under 0<=I<J<len; arbitrary indices are not justified.",
        )
    if line in {145, 146}:
        return (
            "UNUSED_PARTIAL_HELPER",
            "lastOrderedPair is unused and accesses len-2/len-1 without a length guard.",
        )
    if line == 154:
        return (
            "LIMITED_TOTAL_ABSTRACTION",
            "Declared total beyond Float-headed/in-bounds ValSeq cases; target calls remain Float-headed and in bounds.",
        )
    if line in {155, 156}:
        return (
            "ACCEPT_ON_GUARDED_DOMAIN",
            "Float ValSeq accessor equation is correct for Float-headed in-bounds inputs.",
        )
    if line == 160:
        return (
            "LIMITED_TOTAL_ABSTRACTION",
            "scanPairsVS is totalized beyond its valid loop-index/Float-list domain.",
        )
    if 162 <= line <= 177:
        return (
            "ACCEPT_ON_LOOP_INDEX_INVARIANT",
            "Equations match one remaining iteration on valid Float-list loop states.",
        )
    if line == 185:
        return (
            "REJECT_RESULT_BEARING_ORACLE",
            "Opaque symbolic projections influence the return and postcondition; only concrete evaluator equations constrain them.",
        )
    if line in {189, 192}:
        return (
            "ACCEPT_CONCRETE_ONLY",
            "Ground evaluator equation agrees with scanPairsVS, but supplies no symbolic universal connection theorem.",
        )
    if line == 201:
        return (
            "REJECT_UNPROVED_OPERATIONAL_BRIDGE",
            "Priority rule skips the real While and writes the exact desired scan summary without a bridge-free proof.",
        )
    return ("REVIEW_ERROR", "Unclassified verification entry.")


with SOURCE.open(newline="") as source, OUTPUT.open("w", newline="") as output:
    reader = csv.DictReader(source, delimiter="\t")
    fieldnames = list(reader.fieldnames or []) + ["use_scope", "assessment", "rationale"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    count = 0
    errors = 0
    for row in reader:
        path = row["file"]
        line = int(row["start_line"])
        if path.startswith("reference-semantics/"):
            row["use_scope"] = (
                "selected-baseline; constructs from this file are on the program path"
                if path in USED_BASELINE_FILES
                else "selected-baseline; unused by this submitted program"
            )
            row["assessment"] = "ACCEPT_FIXED_SUPPLIED_BASELINE"
            row["rationale"] = (
                "Byte-identical to the trusted supplied semantics; it defines the selected semantics level. "
                "Program-used behavior is separately mapped in REVIEW.md."
            )
        elif path == "verification.k":
            row["use_scope"] = "proof-local extension"
            row["assessment"], row["rationale"] = verification_assessment(line)
        elif path == "spec.k":
            row["use_scope"] = "target entry claim"
            row["assessment"] = "RESULT_CONSTRAINING_BUT_ASSUMPTION_DEPENDENT"
            row["rationale"] = (
                "The postcondition is discriminating, but repeats the same opaque closest* terms written by the loop bridge."
            )
        else:
            row["use_scope"] = "unknown"
            row["assessment"] = "REVIEW_ERROR"
            row["rationale"] = "Unexpected inventory path."
        errors += row["assessment"] == "REVIEW_ERROR"
        writer.writerow(row)
        count += 1

print(f"reviewed_rows={count}")
print(f"review_errors={errors}")
print(f"output={OUTPUT}")
raise SystemExit(1 if errors else 0)
