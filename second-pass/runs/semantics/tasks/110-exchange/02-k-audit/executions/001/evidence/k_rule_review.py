#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventoried K item."""

from __future__ import annotations

import csv
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/k-rule-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/k-rule-review.tsv")

# Start lines of fixed-semantics rules on the execution slice of solution.mpy.
RELEVANT_FIXED_RULES = {
    "reference-semantics/semantics/core.k": {
        125,
        126,
        127,
        131,
        132,
        158,
        189,
        190,
        191,
        194,
        202,
        214,
        215,
    },
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 85},
    "reference-semantics/semantics/call.k": {20, 21, 69},
    "reference-semantics/semantics/controls.k": {
        9,
        20,
        52,
        53,
        54,
        69,
        71,
        72,
        73,
    },
    "reference-semantics/semantics/tuple.k": {32},
    "reference-semantics/semantics/operators.k": {12, 17},
    "reference-semantics/semantics/int.k": {9, 15, 20, 23, 26, 27},
    "reference-semantics/semantics/str.k": {14, 15, 16},
}

LOCAL_RULE_REVIEW = {
    10: (
        "SOUND_OPERATIONAL_EXTENSION",
        "Empty intVals iterator yields #iterDone; exact empty case, no cells changed, "
        "and the continuation is framed unchanged.",
    ),
    11: (
        "SOUND_OPERATIONAL_EXTENSION",
        "Nonempty intVals iterator yields its integer head and intVals tail; exact "
        "constructor recursion, no cells changed, disjoint from the fixed .ValSeq/vCons cases.",
    ),
    18: (
        "SOUND_DEFINITION",
        "oddAcc base returns the incoming accumulator.",
    ),
    19: (
        "SOUND_DEFINITION",
        "Even head leaves odd accumulator unchanged; guard is the pyMod(I,2)=0 branch.",
    ),
    21: (
        "SOUND_DEFINITION",
        "Odd head increments the accumulator; guard complements the zero-modulo branch.",
    ),
    25: (
        "SOUND_DEFINITION",
        "evenAcc base returns the incoming accumulator.",
    ),
    26: (
        "SOUND_DEFINITION",
        "Even head increments the accumulator under pyMod(I,2)=0.",
    ),
    28: (
        "SOUND_DEFINITION",
        "Odd head leaves the even accumulator unchanged under the complementary guard.",
    ),
    32: (
        "SOUND_DEFINITION",
        "Returns ASCII YES exactly when the odd count is at most the donor even count.",
    ),
    35: (
        "SOUND_DEFINITION",
        "Returns ASCII NO on the complementary strict-greater branch.",
    ),
    42: (
        "SOUND_MACRO",
        "Exact AST of the submitted first-loop body; compile-time expansion only.",
    ),
    50: (
        "SOUND_MACRO",
        "Exact AST of the submitted second-loop body; compile-time expansion only.",
    ),
    58: (
        "SOUND_MACRO",
        "Exact full FuncDef AST regenerated in solution.mpy; compile-time expansion does not bypass execution.",
    ),
}

CLAIM_REVIEW = {
    7: (
        "SOUND_AUXILIARY_CLAIM",
        "Nonempty first-loop induction claim steps the real #loop and exact body, "
        "updates only odd and the dead final loop variable, and preserves arbitrary continuation.",
    ),
    37: (
        "SOUND_AUXILIARY_CLAIM",
        "Nonempty second-loop induction claim steps the real #loop and exact body, "
        "updates only even and the dead final loop variable, and preserves arbitrary continuation.",
    ),
    68: (
        "SOUND_RESULT_CONSTRAINING_ENTRY_CLAIM",
        "Loads and calls the exact function body from the exact initial configuration; "
        "the final k value is the total YES/NO summary for nonempty integer sequences.",
    ),
}


with INVENTORY.open(newline="") as source, OUTPUT.open("w", newline="") as target:
    reader = csv.DictReader(source, delimiter="\t")
    assert reader.fieldnames is not None
    fieldnames = reader.fieldnames + [
        "on_solution_execution_slice",
        "disposition",
        "audit_rationale",
    ]
    writer = csv.DictWriter(target, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()

    counts: dict[str, int] = {}
    for row in reader:
        path = row["file"]
        line = int(row["line"])
        on_slice = False

        if path == "verification.k" and row["kind"] == "rule":
            disposition, rationale = LOCAL_RULE_REVIEW[line]
            on_slice = True
        elif path == "spec.k" and row["kind"] == "claim":
            disposition, rationale = CLAIM_REVIEW[line]
            on_slice = True
        elif path.startswith("reference-semantics/"):
            if (
                row["kind"] == "rule"
                and line in RELEVANT_FIXED_RULES.get(path, set())
            ):
                on_slice = True
                disposition = "SOUND_FIXED_RULE_ON_EXECUTION_SLICE"
                rationale = (
                    "Byte-identical supplied-semantics rule; inspected in the "
                    "load/call/binding/loop/operator/return execution slice and "
                    "consistent with its selected MPY semantics role."
                )
            elif row["kind"] == "rule":
                disposition = "FIXED_RULE_NOT_REACHED"
                rationale = (
                    "Byte-identical supplied-semantics rule for a construct or "
                    "value form absent from solution.mpy; it is not a candidate "
                    "proof extension and cannot contribute to this claim's closure."
                )
            else:
                disposition = "FIXED_DECLARATION_ACCEPTED"
                rationale = (
                    "Byte-identical selected supplied-semantics declaration/import."
                )
        elif path == "verification.k":
            disposition = "LOCAL_DECLARATION_REVIEWED"
            rationale = (
                "Constructor/function/macro declaration corresponding to the "
                "separately reviewed local rules; no functional, simplification, "
                "priority, concrete, or owise attribute is hidden here."
            )
            on_slice = True
        elif path == "spec.k":
            disposition = "SPEC_STRUCTURE_REVIEWED"
            rationale = "Spec module/import wrapper; substantive claims are reviewed separately."
        else:
            raise AssertionError((path, line))

        counts[disposition] = counts.get(disposition, 0) + 1
        row.update(
            {
                "on_solution_execution_slice": str(on_slice).lower(),
                "disposition": disposition,
                "audit_rationale": rationale,
            }
        )
        writer.writerow(row)

print(f"review_path={OUTPUT}")
for key in sorted(counts):
    print(f"{key}={counts[key]}")
