#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventoried K record."""

from __future__ import annotations

from collections import Counter
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/04_rule_inventory.txt")

ACTIVE_RANGES: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/syntax.k": [
        (9, 16), (22, 22), (28, 32), (41, 41), (49, 50), (53, 61)
    ],
    "reference-semantics/semantics/core.k": [
        (13, 42), (49, 60), (68, 70), (117, 127), (130, 191),
        (194, 215), (223, 225)
    ],
    "reference-semantics/semantics/functions.k": [(8, 20), (62, 90)],
    "reference-semantics/semantics/call.k": [(15, 50), (69, 75)],
    "reference-semantics/semantics/controls.k": [(8, 18), (46, 54)],
    "reference-semantics/semantics/builtins.k": [(17, 26)],
    "reference-semantics/semantics/sort.k": [(14, 42)],
    "reference-semantics/semantics/operators.k": [(10, 46)],
    "reference-semantics/semantics/int.k": [(7, 27)],
    "reference-semantics/semantics/float.k": [(19, 32)],
    "reference-semantics/semantics/subscript.k": [(6, 41)],
}


def in_ranges(path: str, line: int) -> bool:
    return any(start <= line <= end for start, end in ACTIVE_RANGES.get(path, []))


def disposition(path: str, line: int, statement: str) -> tuple[str, str]:
    if path == "verification.k":
        if line == 9:
            return (
                "ACCEPT_CONDITIONAL_EXTENSION",
                "length preservation is true under the supplied sortVS-as-permutation contract",
            )
        if line in (13, 14, 15, 16):
            return (
                "ACCEPT_PROOF_LOCAL_DEFINITION",
                "structural all-integer predicate has disjoint exhaustive equations",
            )
        if line == 21:
            return (
                "LIMITATION_RESULT_OPAQUE",
                "fresh total Int-valued symbol has no independent value equations",
            )
        if line == 23:
            return (
                "LIMITATION_DEFINITIONAL_ALIAS",
                "guarded alias is plausible for sorted integer inputs but lacks a bridge-free K connection theorem",
            )
        return ("REVIEW_ERROR", "unexpected verification record")

    if path == "spec.k":
        return (
            "REJECT_INTENT_ADEQUACY",
            "claim executes the candidate but narrows the domain and the even formula disagrees with canonical median",
        )

    if path == "reference-semantics/semantics/sort.k" and "sortVS(" in statement:
        if line == 18:
            return (
                "ACTIVE_TRUSTED_PRIMITIVE",
                "opaque symbolic ascending-sort/permutation contract; concrete insertion-sort twin",
            )
        if in_ranges(path, line):
            return (
                "ACTIVE_FIXED_ACCEPT",
                "used sorted(list) rule or concrete twin; guards and state footprint match the supplied subset",
            )

    if path == "reference-semantics/semantics/float.k" and "intFloatDiv" in statement:
        return (
            "ACTIVE_TRUSTED_PRIMITIVE",
            "opaque symbolic integer/float division with concrete LLVM twin",
        )

    if in_ranges(path, line):
        return (
            "ACTIVE_FIXED_ACCEPT",
            "used declaration/rule follows the supplied deterministic subset on integer-list calls; no false witness found",
        )

    if "opaque" in statement or "no-evaluators" in statement:
        return (
            "INERT_TRUSTED_PRIMITIVE",
            "imported but unreachable from the submitted program and claims",
        )
    return (
        "INERT_FIXED_ACCEPT",
        "inventoried and unreachable from the submitted program/claims; no false conclusion witness found",
    )


def main() -> int:
    text = INVENTORY.read_text().splitlines()
    try:
        start = text.index("path\tline\tkind\tclassification\tstatement") + 1
        end = text.index("RECORDS_END")
    except ValueError as err:
        raise SystemExit(f"malformed inventory: {err}")

    counter: Counter[str] = Counter()
    rows: list[str] = []
    for raw in text[start:end]:
        path, line_text, kind, classification, statement = raw.split("\t", 4)
        decision, rationale = disposition(path, int(line_text), statement)
        counter[decision] += 1
        rows.append(
            "\t".join(
                [path, line_text, kind, classification, decision, rationale, statement]
            )
        )

    print("K RULE/DECLARATION ASSESSMENT")
    print(f"RECORDS\t{len(rows)}")
    for decision in sorted(counter):
        print(f"DECISION\t{decision}\t{counter[decision]}")
    print("ASSESSMENTS_BEGIN")
    print("path\tline\tkind\tclassification\tdecision\trationale\tstatement")
    print("\n".join(rows))
    print("ASSESSMENTS_END")
    return 1 if counter["REVIEW_ERROR"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
