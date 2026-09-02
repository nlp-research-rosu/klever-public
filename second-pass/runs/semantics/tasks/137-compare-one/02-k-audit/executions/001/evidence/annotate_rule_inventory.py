#!/usr/bin/env python3
"""Attach an explicit reviewer disposition to every inventoried K declaration."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


SOURCE = Path("/audit-output/evidence/rule-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/rule-review.tsv")
SUMMARY = Path("/audit-output/evidence/rule-review-summary.json")


# Lines on the real runCompare path. Whole syntax/configuration declarations that
# define a used sort are conservatively included.
USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/syntax.k": [(7, 62)],
    "reference-semantics/semantics/core.k": [
        (13, 60),
        (123, 215),
    ],
    "reference-semantics/semantics/call.k": [(15, 32), (69, 75)],
    "reference-semantics/semantics/functions.k": [(62, 90)],
    "reference-semantics/semantics/controls.k": [(8, 18), (50, 54)],
    "reference-semantics/semantics/builtins.k": [(287, 297)],
    "reference-semantics/semantics/methods.k": [(9, 10), (104, 109)],
    "reference-semantics/semantics/operators.k": [(14, 20)],
    "reference-semantics/semantics/int.k": [(1, 28)],
    "reference-semantics/semantics/float.k": [
        (19, 21),
        (41, 44),
        (123, 164),
        (185, 206),
    ],
    "reference-semantics/semantics/str.k": [(12, 17)],
}


def intersects(start: int, end: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= upper and end >= lower for lower, upper in ranges)


def verification_disposition(line: int) -> tuple[str, str, str]:
    if line == 11:
        return (
            "ILLEGITIMATE_RESULT_ORACLE",
            "commaDecimal is total/result-bearing but has no defining or connection equation.",
            'For a="2,3", b=1, the admitted interpretation commaDecimal("2,3")=0.0 '
            'with faithful comparisons returns 1; fixed semantics and Python return "2,3".',
        )
    if line == 13:
        return ("INTERNAL_MARKER", "Continuation tag only; it has no value meaning by itself.", "")
    if line in (14, 19):
        return (
            "UNSOUND_UNCONNECTED_OPERATIONAL_BRIDGE",
            "Preempts float(str.replace) and fabricates commaDecimal without a bridge-free "
            "universal connection theorem; the line-14 match also ignores callee binding.",
            'For a="2,3", b=1, interpret commaDecimal("2,3") as 0.0: the bridged program '
            'can return 1 although fixed semantics/Python return "2,3".',
        )
    if line == 24:
        return (
            "ILLEGITIMATE_RESULT_ORACLE",
            "sameFloat is total/result-bearing but has no defining or connection equation.",
            "For a=1.0,b=2.0, sameFloat(1.0,2.0)=true drives return noneV, "
            "while fixed float equality is false and Python returns 2.0.",
        )
    if line == 26:
        return (
            "UNSOUND_UNCONNECTED_OPERATIONAL_BRIDGE",
            "Preempts supplied Float equality and replaces it with unconnected sameFloat.",
            "For a=1.0,b=2.0, sameFloat(1.0,2.0)=true yields noneV instead of 2.0.",
        )
    if line == 34:
        return ("ENTRY_WRAPPER_SYNTAX", "Fresh entry syntax; no behavior by itself.", "")
    if line == 35:
        return (
            "EXACT_BODY_WRAPPER_WITH_FORMAL_PINNING_GAP",
            "Expands to an exact textual copy of the translated body and uses normal closure "
            "machinery, but the theorem never loads solution.mpy and has no body-identity claim.",
            "",
        )
    if line in (60, 61, 62, 63):
        return (
            "SOUND_DEFINITION_ON_ENTRY_DOMAIN",
            "numericValue equations are truthful for the three entry sorts; the function is "
            "intentionally partial on other Val constructors.",
            "",
        )
    if line in (65, 66, 67, 68, 69):
        return (
            "STRUCTURALLY_SOUND_CONDITIONAL_SUMMARY",
            "The sort-disjoint equations mirror the program comparison shape, conditional on "
            "the fixed opaque float primitives and candidate sameFloat.",
            "",
        )
    if line in (73, 74):
        return (
            "CONDITIONAL_POSTCONDITION_NOT_INTENDED_RESULT",
            "The if-then-else shape is mathematical, but its result depends on unconnected "
            "commaDecimal/sameFloat and therefore is not the requested concrete comparison.",
            "",
        )
    return ("UNCLASSIFIED_VERIFICATION_RECORD", "Manual routing gap.", "")


def main() -> int:
    with SOURCE.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        base_fields = list(reader.fieldnames or [])

    reviewed = []
    counts: Counter[str] = Counter()
    for row in rows:
        file_name = row["file"]
        start = int(row["start_line"])
        end = int(row["end_line"])
        witness = ""
        if file_name.startswith("reference-semantics/"):
            if intersects(start, end, USED_RANGES.get(file_name, [])):
                disposition = "SUPPLIED_FIXED_SEMANTICS_USED"
                rationale = (
                    "Byte-identical to the trusted supplied semantics. This declaration/rule is "
                    "on the submitted body's path; its evaluation/control/state role was checked "
                    "against the program construct. Float no-evaluator symbols remain explicit "
                    "fixed-semantics trust boundaries."
                )
            else:
                disposition = "SUPPLIED_FIXED_SEMANTICS_UNUSED"
                rationale = (
                    "Byte-identical to the trusted supplied semantics and not reachable from the "
                    "submitted body/entry claims. No candidate-local alteration or proof "
                    "dependency; no narrower false-rule witness was found in this audit."
                )
        elif file_name == "verification.k":
            disposition, rationale, witness = verification_disposition(start)
        elif file_name == "spec.k":
            disposition = "CLOSES_BUT_ORACLE_RELATIVE_ENTRY_CLAIM"
            rationale = (
                "Unconditional sort-pair claim with satisfiable inputs. It closes, but its RHS "
                "expectedCompare shares the candidate's unconnected result-bearing oracles."
            )
        else:
            disposition = "UNCLASSIFIED"
            rationale = "No reviewer classification."
        counts[disposition] += 1
        row.update(
            {
                "review_disposition": disposition,
                "review_rationale": rationale,
                "false_conclusion_witness": witness,
            }
        )
        reviewed.append(row)

    fields = base_fields + [
        "review_disposition",
        "review_rationale",
        "false_conclusion_witness",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(reviewed)

    summary = {
        "record_count": len(reviewed),
        "dispositions": dict(sorted(counts.items())),
        "unclassified_count": sum(
            count for name, count in counts.items() if "UNCLASSIFIED" in name
        ),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if summary["unclassified_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
