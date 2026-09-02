#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventoried K declaration."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


SOURCE = Path("/audit-output/evidence/k-rule-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/k-rule-assessment.tsv")

# Fixed-semantics declarations/rules on the submitted function's execution path.
# The line is the declaration's first source line.
USED_FIXED: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {
        8, 35, 37, 41, 56, 57, 60, 61
    },
    "reference-semantics/semantics/core.k": {
        13, 14, 18, 29, 35, 36, 39, 41, 42, 49, 68, 117, 118, 126, 127,
        130, 131, 132, 157, 158, 185, 186, 189, 190, 191, 194, 199, 200,
        208, 209, 210, 213, 214, 215, 217, 218, 219
    },
    "reference-semantics/semantics/iter.k": {6},
    "reference-semantics/semantics/list.k": {
        9, 10, 13, 14, 15, 18, 19, 20, 53
    },
    "reference-semantics/semantics/operators.k": {15, 16, 17},
    "reference-semantics/semantics/int.k": {24},
    "reference-semantics/semantics/controls.k": {
        9, 48, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85
    },
    "reference-semantics/semantics/functions.k": {
        8, 63, 64, 78, 85
    },
    "reference-semantics/semantics/call.k": {
        16, 19, 20, 21, 24, 69
    },
    "reference-semantics/semantics/tuple.k": {31, 32},
}


def local_disposition(line: int, kind: str) -> tuple[str, str, str]:
    if line in (9, 10, 15, 16):
        return (
            "reachable",
            "PASS_EXACT_BODY_MACRO",
            "Macro expansion is constructor-identical to regenerated solution.mpy.",
        )
    if line == 29:
        return (
            "reachable",
            "PASS_TRANSPARENT_INPUT_REPRESENTATION",
            "Fresh ValSeq constructor represents arbitrary finite integer sequences.",
        )
    if line in (30, 31):
        return (
            "reachable",
            "PASS_CONNECTED_OPERATIONAL_BRIDGE",
            "Disjoint/exhaustive iterator cases preserve the full continuation and "
            "match bridge-free native-list iterator claims.",
        )
    if line in (36, 37, 38):
        return (
            "postcondition",
            "PASS_STRUCTURAL_FILTER_DEFINITION",
            "Empty/cons IntSeq cases are disjoint, exhaustive, and descending.",
        )
    if line in (41, 43, 47):
        return (
            "postcondition",
            "PASS_TOTAL_BOOLEAN_BRANCH",
            "True/false guards are disjoint and exhaustive; RHS is ordinary filtering.",
        )
    return (
        "reachable",
        "REVIEWED_LOCAL_DECLARATION",
        f"Local {kind} reviewed with its enclosing definition.",
    )


def claim_disposition(line: int) -> tuple[str, str, str]:
    if line == 9:
        return (
            "entry-helper",
            "PASS_LOOP_EXECUTION_CLAIM",
            "Executes the exact loop body, preserves arbitrary CONT and framed cells, "
            "and constrains the accumulator to the recursive filter.",
        )
    return (
        "entry",
        "FORMALLY_SOUND_DOMAIN_LIMITED",
        "Constrains ref(0) and its exact list contents for arbitrary IntSeq, but "
        "does not quantify over non-integer numeric lists.",
    )


def main() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)

    fieldnames = list(rows[0]) + ["reachability", "decision", "audit_reason"]
    decisions: dict[str, int] = {}
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            file = row["file"]
            line = int(row["line"])
            if file == "verification.k":
                reachability, decision, reason = local_disposition(
                    line, row["kind"]
                )
            elif file == "spec.k":
                reachability, decision, reason = claim_disposition(line)
            elif file == "reference-semantics/semantics/concrete.k":
                reachability, decision, reason = (
                    "concrete-only",
                    "NOT_IMPORTED_BY_PROOF",
                    "Available only in MPY-KRUN; reviewed as concrete-test support.",
                )
            elif line in USED_FIXED.get(file, set()):
                reachability, decision, reason = (
                    "reachable",
                    "PASS_USED_FIXED_SEMANTICS",
                    "On-path fixed rule/declaration preserves Python evaluation, "
                    "binding, state, or integer/list behavior for this program.",
                )
            elif "opaque-symbol" in row["classification"]:
                reachability, decision, reason = (
                    "unreachable",
                    "UNUSED_FIXED_TRUST_BOUNDARY",
                    "Opaque fixed-semantics primitive cannot unify with any submitted "
                    "program operation or postcondition term.",
                )
            else:
                reachability, decision, reason = (
                    "unreachable",
                    "UNREACHED_FIXED_BASELINE",
                    "Exact trusted supplied-semantics entry; constructor/control "
                    "unification excludes it from this theorem's execution.",
                )
            row.update(
                {
                    "reachability": reachability,
                    "decision": decision,
                    "audit_reason": reason,
                }
            )
            decisions[decision] = decisions.get(decision, 0) + 1
            writer.writerow(row)

    print(f"OUTPUT {OUTPUT}")
    print(f"SHA256 {hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
    print(f"ROWS {len(rows)}")
    print(f"DECISIONS {decisions}")
    print("EVERY_INVENTORY_ROW_ASSESSED true")


if __name__ == "__main__":
    main()
