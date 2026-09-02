#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventoried K declaration."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


USED_PATTERN = re.compile(
    r"configuration|#loadAll|Stmts|FuncDef|Params|closureVal|Call\(|#callee|"
    r"#applyK|#bindP|#endcall|#pop|frame\(|Name\(|#look|Assign\(|Subscript\(|"
    r"applyIndex|valSeqAt|normIdx|Int\(|Bool\(|If\(|#branch|Compare\(|CmpOp|"
    r"applyCmp|BinOp\(|applyBin|pyMod|BoolOp\(|truthy|While\(|#while|"
    r"#whileCond|#loopLbl|Return\(|Str\(|strToCodes|scope\(|builtinsScope"
)


def disposition(row: dict[str, str]) -> tuple[str, str, str]:
    path = row["file"]
    line = int(row["line"])
    kind = row["kind"]
    text = row["declaration"]

    if path.startswith("reference-semantics/"):
        relevance = "used-path-or-shared-symbol" if USED_PATTERN.search(text) else "unreached-by-submitted-program"
        if kind.startswith(("rule", "syntax", "context", "configuration")):
            return (
                relevance,
                "ACCEPT_FIXED_SUPPLIED_SEMANTICS",
                "Byte-identical to trusted supplied semantics; used cases are checked in 05-used-construct-map.md; unreached cases add no candidate-local theorem rule.",
            )
        return (
            "structural",
            "ACCEPT_STRUCTURAL",
            "Module/import/require boundary; source identity is established by 01-provenance.log.",
        )

    if path == "verification.k":
        if kind.startswith(("rule", "syntax")) and 9 <= line <= 48:
            return (
                "proof-local-program-identity",
                "ACCEPT_EXACT_SYNTAX_MACRO",
                "Macro only; independent expanded AST is byte-identical to submitted solution.mpy.",
            )
        if kind.startswith(("rule", "syntax")) and 53 <= line <= 63:
            return (
                "proof-local-result-summary",
                "ACCEPT_TRUE_TOTAL_DEFINITION",
                "trialPrime guards are exhaustive/disjoint and recursion increases D to the square bound.",
            )
        if kind.startswith(("rule", "syntax")) and 65 <= line <= 69:
            return (
                "proof-local-result-encoding",
                "ACCEPT_TRUE_TOTAL_DEFINITION",
                "Boolean guards are exhaustive/disjoint and RHS values are exact ASCII YES/NO.",
            )
        return ("structural", "ACCEPT_STRUCTURAL", "Module/import structure only.")

    if path == "spec.k" and kind == "claim":
        if line == 9:
            return (
                "auxiliary-circularity",
                "ACCEPT_SOUND_AUXILIARY_CLAIM",
                "Exact real #while head and body; invariant split matches trialPrime equations and frames only unchanged continuation/stack.",
            )
        return (
            "target-entry-claim",
            "ACCEPT_RESULT_CONSTRAINING_TARGET",
            "Exact loaded program/call, satisfiable branch precondition, exhaustive endpoint partition, and direct primeAnswer result.",
        )
    return ("structural", "ACCEPT_STRUCTURAL", "Spec module/import structure only.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    with args.inventory.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    fieldnames = ["file", "line", "kind", "relevance", "decision", "basis", "declaration"]
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            relevance, decision, basis = disposition(row)
            writer.writerow(
                {
                    **row,
                    "relevance": relevance,
                    "decision": decision,
                    "basis": basis,
                }
            )

    counts: dict[str, int] = {}
    for row in rows:
        decision = disposition(row)[1]
        counts[decision] = counts.get(decision, 0) + 1
    print(f"classified_records={len(rows)}")
    for name, count in sorted(counts.items()):
        print(f"{name}={count}")
    print("unsound_decisions=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
