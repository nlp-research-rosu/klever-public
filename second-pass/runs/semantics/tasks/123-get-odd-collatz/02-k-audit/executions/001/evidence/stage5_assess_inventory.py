#!/usr/bin/env python3
"""Attach an audit disposition to every Stage-5 inventory record."""

from __future__ import annotations

import csv
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/stage5_inventory.tsv")

# Explicit operational/equational rules exercised by the submitted program and
# its claims. Compiler-generated heating/cooling is tracked through the syntax
# declarations and contexts rather than source `rule` line numbers.
USED_RULES: dict[str, set[int]] = {
    "reference-semantics/semantics/core.k": {
        118,
        125,
        126,
        127,
        131,
        132,
        152,
        158,
        189,
        190,
        191,
        194,
        200,
        202,
        214,
        215,
        218,
        219,
        224,
        225,
    },
    "reference-semantics/semantics/operators.k": {12, 17},
    "reference-semantics/semantics/int.k": {9, 14, 15, 16, 20, 26, 27},
    "reference-semantics/semantics/list.k": {14, 15, 19, 20, 53},
    "reference-semantics/semantics/controls.k": {
        9,
        48,
        52,
        53,
        54,
        77,
        78,
        79,
        81,
        85,
    },
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 80, 85},
    "reference-semantics/semantics/call.k": {16, 20, 21, 31, 38, 69},
    "reference-semantics/semantics/sort.k": {20, 21, 22, 23, 24, 36},
}

CLAIM_DECISIONS = {
    7: (
        "CLOSED_LOCAL_EXECUTION",
        "odd-step is satisfiable and exactly executes one real odd branch; it is not an entry theorem.",
    ),
    56: (
        "CLOSED_LOCAL_EXECUTION",
        "even-step is satisfiable and exactly executes one real even branch; it is not an entry theorem.",
    ),
    104: (
        "CLOSED_LOCAL_EXECUTION",
        "exit-step is satisfiable and executes loop exit, append, sorted, return, and frame pop.",
    ),
    147: (
        "CLOSED_CONCRETE_ENTRY",
        "Complete result-constraining execution for input 1 only.",
    ),
    174: (
        "CLOSED_CONCRETE_ENTRY",
        "Complete result-constraining execution for input 5 only.",
    ),
    200: (
        "CLOSED_CONCRETE_ENTRY",
        "Complete result-constraining execution for input 6 only.",
    ),
    226: (
        "CLOSED_CONCRETE_ENTRY",
        "Complete result-constraining execution for input 7 only.",
    ),
}


def disposition(row: dict[str, str]) -> tuple[str, str]:
    file = row["file"]
    line = int(row["line"])
    kind = row["kind"]
    flags = row["flags"]

    if file == "verification.k":
        if kind == "rule" and line == 8:
            return (
                "ACCEPT_EXACT_ABBREVIATION",
                "#getOddCollatz expands to the exact hard-coded submitted MPY term plus its call; it does not skip execution.",
            )
        if kind == "rule" and line in {30, 33, 39}:
            return (
                "ACCEPT_UNUSED_DEFINITION",
                "Truthful, guard-disjoint Collatz recurrence, but no claim mentions collatzResult, so it contributes to no proof.",
            )
        if kind == "rule" and line == 46:
            return (
                "ACCEPT_EXACT_ABBREVIATION",
                "getOddCollatzClosure unfolds to the exact closure installed by the submitted function definition.",
            )
        return (
            "PROOF_LOCAL_DECLARATION",
            "Declaration/import only; no priority, simplification, totality, or opaque proof-local axiom is present.",
        )

    if file == "spec.k" and kind == "claim":
        return CLAIM_DECISIONS[line]
    if file == "spec.k":
        return (
            "SPEC_STRUCTURE",
            "Module/import structure only; no additional rule or axiom.",
        )

    if file.startswith("reference-semantics/"):
        if file == "reference-semantics/semantics/sort.k" and kind == "syntax" and line in {
            18,
            49,
        }:
            if line == 18:
                return (
                    "TRUSTED_RESULT_BOUNDARY_USED",
                    "sortVS is opaque in Haskell and concrete in LLVM; entry results are conditional on it meaning ascending sort.",
                )
            return (
                "TRUSTED_OPAQUE_UNUSED",
                "sortKeyVS is an explicit supplied-semantics opaque primitive, unreachable from this program.",
            )
        if "opaque-no-evaluators" in flags:
            return (
                "TRUSTED_OPAQUE_UNUSED",
                "Explicit supplied-semantics opaque symbol; unreachable from the submitted integer/list/sorted fragment.",
            )
        if kind == "rule" and line in USED_RULES.get(file, set()):
            if file == "reference-semantics/semantics/sort.k" and line in {
                20,
                21,
                22,
                23,
                24,
            }:
                return (
                    "SUPPLIED_CONCRETE_SORT_RULE_USED",
                    "Concrete-only insertion-sort equation used by LLVM; guards are disjoint and recursion descends.",
                )
            return (
                "SUPPLIED_USED_RULE_ACCEPTED",
                "Rule is in the real execution slice; binding, evaluation order, cell footprint, and arithmetic match the submitted program.",
            )
        if kind in {"syntax", "context", "configuration"}:
            return (
                "SUPPLIED_DECLARATION_REVIEWED",
                "Byte-identical fixed supplied-semantics declaration; used constructs are mapped separately and no proof-local behavior is introduced.",
            )
        if kind == "rule":
            return (
                "SUPPLIED_RULE_NOT_REACHED",
                "Byte-identical fixed supplied-semantics rule outside the submitted program/proof slice; it contributes to no claimed conclusion and no false-rule witness was identified.",
            )
        return (
            "SUPPLIED_ASSEMBLY",
            "Byte-identical fixed supplied-semantics module/import/require structure.",
        )

    return ("UNCLASSIFIED", "Unexpected inventory record.")


with INVENTORY.open(newline="", encoding="utf-8") as source:
    reader = csv.DictReader(source, delimiter="\t")
    print("id\tfile\tline\tkind\tflags\tdecision\treason")
    for row in reader:
        decision, reason = disposition(row)
        print(
            "\t".join(
                [
                    row["id"],
                    row["file"],
                    row["line"],
                    row["kind"],
                    row["flags"],
                    decision,
                    reason,
                ]
            )
        )
