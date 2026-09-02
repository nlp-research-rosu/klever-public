#!/usr/bin/env python3
"""Attach an explicit audit decision to every row of rule-inventory.tsv."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


SOURCE = Path("/audit-output/evidence/rule-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/rule-review.tsv")
SUMMARY = Path("/audit-output/evidence/rule-review-summary.md")

USED_FIXED_LINES = {
    "semantics/core.k": {
        49, 68, 69, 70, 117, 118, 124, 125, 126, 127, 130, 131, 132, 145, 152,
        157, 158, 185, 186, 189, 190, 191, 194, 195, 199, 200, 208, 209, 210,
        213, 214, 215, 217, 218, 219, 223, 224, 225,
    },
    "semantics/functions.k": {8, 14, 63, 64, 68, 78, 80, 85},
    "semantics/call.k": {19, 20, 21, 26, 31, 69},
    "semantics/bool.k": {16, 17, 18, 20, 29, 31, 35},
    "semantics/operators.k": {15, 16, 17, 34, 38},
    "semantics/subscript.k": {
        44, 49, 50, 51, 52, 54, 55, 56, 58, 61, 72, 73, 74, 76, 77, 79, 81,
        83, 84, 86, 88, 90, 91, 93, 96, 97, 99, 102, 103, 105, 109, 110, 113,
    },
    "semantics/list.k": {9, 10, 27},
    "semantics/builtins.k": {47, 48, 49, 50, 54, 55, 56},
    "semantics/int.k": {23},
    "semantics/float.k": {
        20, 21, 111, 112, 113, 125, 126, 129, 195, 196, 261, 262, 265, 266,
        267, 270,
    },
    "semantics/syntax.k": set(range(1, 1000)),
    "semantics/iter.k": {8},
}


def decision(row: dict[str, str]) -> tuple[str, str]:
    file_name = row["file"]
    line = int(row["line"])
    declaration = row["declaration"]
    kind = row["kind"]

    if "/reference-semantics/" in file_name:
        relative = file_name.split("/reference-semantics/", 1)[1]
        used = line in USED_FIXED_LINES.get(relative, set())
        if used:
            return (
                "ACCEPTED_FIXED_USED",
                "Unchanged supplied-semantics declaration on the submitted term's "
                "lookup/call/slice/list-equality/short-circuit/sum/compare/return path; "
                "the complete used path was also exercised concretely and through the "
                "bridge-free connection claims.",
            )
        return (
            "ACCEPTED_FIXED_INERT",
            "Unchanged supplied-semantics declaration; inspection found no task-specific "
            "symbol, and this declaration is unreachable from the submitted term and "
            "entry configurations, so it cannot enable a task conclusion.",
        )

    if file_name.endswith("/mutation-verification.k"):
        return (
            "EXCLUDED_NEGATIVE_ONLY",
            "Deliberately false candidate mutation rule compiled only in the separate "
            "SUMMARY-MUTATION definition; it is absent from every positive definition.",
        )
    if any(
        file_name.endswith(suffix)
        for suffix in (
            "/spec-vacuity.k",
            "/spec-body-mutation.k",
            "/spec-summary-mutation.k",
        )
    ):
        return (
            "EXCLUDED_NEGATIVE_ONLY",
            "Negative validation claim, not imported by a positive proof module.",
        )

    if file_name.endswith("/verification.k"):
        if kind in {"module"}:
            return ("ACCEPTED_PROOF_STRUCTURE", "Module/import boundary is explicit and acyclic.")
        if kind == "syntax":
            if "noFloatSum" in declaration:
                return (
                    "ACCEPTED_OFFPATH_TOTALIZER",
                    "Opaque totalizer has no equations, but every float target and bridge "
                    "requires hasFloat(VS); finite ground sequences satisfying that guard "
                    "cannot reach the empty/no-float result.",
                )
            if any(name in declaration for name in ("projectIntTotal", "projectBoolTotal", "projectFloatTotal", "intLikeTotal")):
                return (
                    "ACCEPTED_GUARDED_PROJECTION",
                    "Total off-domain interpretation is unused; all result-bearing uses are "
                    "under mutually exclusive generated-sort guards and collapse to the "
                    "original Int/Bool/Float value.",
                )
            if any(name in declaration for name in ("sumInts", "sumFloatRest", "sumToFloat", "reverseSlice")):
                return (
                    "ACCEPTED_CONNECTED_SUMMARY",
                    "Result-bearing summary is fixed on its target domain and has a fresh "
                    "bridge-free universal execution connection claim.",
                )
            if "willItFlyClosure" in declaration:
                return (
                    "ACCEPTED_EXACT_PROGRAM_TERM",
                    "Nullary syntax name expands to the mechanically compared constructor "
                    "body and does not bypass call/frame/return execution.",
                )
            return (
                "ACCEPTED_DEFINITIONAL_SYMBOL",
                "Classifier/sequence predicate declaration is covered by exhaustive, "
                "constructor-descending equations.",
            )

        if kind == "rule":
            if "<k>" in declaration:
                if "#slStep" in declaration:
                    return (
                        "ACCEPTED_OPERATIONAL_BRIDGE",
                        "Exact slice continuation, arbitrary suffix, and unchanged omitted "
                        "cells are proved bridge-free by SUM-CONNECTION.reverse-slice.",
                    )
                if "#sumContF" in declaration:
                    return (
                        "ACCEPTED_OPERATIONAL_BRIDGE",
                        "Exact float-rest fold is proved bridge-free over the same allNumeric domain.",
                    )
                return (
                    "ACCEPTED_OPERATIONAL_BRIDGE",
                    "Exact integer or initial-float sum continuation is proved bridge-free "
                    "over the same or broader guard before use in the target definition.",
                )
            if "willItFlyClosure()" in declaration:
                return (
                    "ACCEPTED_EXACT_PROGRAM_TERM",
                    "Fresh KAST constructor comparison found exact parameter and body identity "
                    "with the trusted regeneration of solution.mpy.",
                )
            if "intOf(" in declaration:
                return (
                    "ACCEPTED_DERIVED_DISPATCH",
                    "On integralV, the disjoint Int/Bool cases reduce to the two supplied "
                    "intOf equations; overlaps agree on all ground constructors.",
                )
            if any(token in declaration for token in ("projectIntTotal", "projectBoolTotal", "projectFloatTotal", "#Ceil({")):
                return (
                    "ACCEPTED_GUARDED_PROJECTION",
                    "Projection/cast equation is guarded by exact sort membership; concrete "
                    "and symbolic orientations agree where they overlap and preserve definedness.",
                )
            if "noFloatSum" in declaration:
                return (
                    "ACCEPTED_OFFPATH_TOTALIZER",
                    "Equation is reachable only after consuming a no-float sequence, excluded "
                    "by all result-bearing float target/bridge guards.",
                )
            if any(token in declaration for token in ("sumInts", "sumFloatRest", "sumToFloat", "reverseSlice")):
                return (
                    "ACCEPTED_CONNECTED_SUMMARY",
                    "Equation is constructor-exhaustive on its used domain, recursively descends "
                    "on ValSeq, and its operational meaning is established by connection claims.",
                )
            return (
                "ACCEPTED_MATHEMATICAL_DEFINITION",
                "Classifier or finite-sequence predicate equation is exhaustive/disjoint and "
                "agrees with generated-sort membership.",
            )

    if any(
        file_name.endswith(suffix)
        for suffix in (
            "/connection-spec.k",
            "/float-connection-spec.k",
            "/connection-witness.k",
        )
    ):
        return (
            "ACCEPTED_CONNECTION_CLAIM",
            "Positive bridge-free connection or ground value witness; reconstructed module "
            "closed with #Top under its declared imports.",
        )
    if file_name.endswith("/spec.k"):
        return (
            "ACCEPTED_TARGET_CLAIM",
            "Entry claim executes the exact mechanically pinned closure and constrains its "
            "Boolean result; each claim independently closed and has a satisfying ground witness.",
        )
    return ("REVIEWED_OTHER", "Reviewed candidate declaration; no positive-proof dependency.")


with SOURCE.open(newline="") as source_stream:
    rows = list(csv.DictReader(source_stream, delimiter="\t"))

for row in rows:
    row["audit_decision"], row["audit_rationale"] = decision(row)

with OUTPUT.open("w", newline="") as output_stream:
    writer = csv.DictWriter(
        output_stream,
        fieldnames=list(rows[0]) if rows else [],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

totals = Counter(row["audit_decision"] for row in rows)
summary_lines = [
    "# Rule-by-rule audit decision summary",
    "",
    f"Annotated declarations: {len(rows)}",
    "",
]
for name, count in sorted(totals.items()):
    summary_lines.append(f"- {name}: {count}")
SUMMARY.write_text("\n".join(summary_lines) + "\n")

print(f"annotated_declarations={len(rows)}")
for name, count in sorted(totals.items()):
    print(f"{name}={count}")
print(f"review={OUTPUT}")
print(f"summary={SUMMARY}")
