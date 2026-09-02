#!/usr/bin/env python3
"""Attach an audit disposition to every row of the generated K inventory."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


SOURCE = Path("/audit-output/evidence/stage5-rule-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/stage5-rule-assessment.tsv")

# Declaration/rule start lines on the fixed-semantics path exercised by the
# submitted constructor term. Lines not listed remain imported but unreachable.
USED_FIXED: dict[str, set[int]] = {
    "semantics/syntax.k": {7, 25, 37, 52, 53, 54, 55, 56, 62},
    "semantics/core.k": {
        3,
        13,
        14,
        15,
        18,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        208,
        209,
        213,
        214,
        215,
    },
    "semantics/iter.k": {3, 6},
    "semantics/list.k": {3, 9, 10},
    "semantics/str.k": {3, 13, 14, 15, 20, 21, 22, 24},
    "semantics/controls.k": {3, 9, 20, 36, 65, 69, 71, 72, 73, 85},
    "semantics/functions.k": {3, 8, 14, 63, 64, 78, 85},
    "semantics/call.k": {10, 19, 20, 21, 69},
    "semantics/tuple.k": {3, 31, 32},
}


def fixed_is_used(path: str, line: int) -> bool:
    for suffix, lines in USED_FIXED.items():
        if path.endswith(suffix) and line in lines:
            return True
    return False


def candidate_assessment(path: str, line: int, kind: str) -> tuple[str, str]:
    if path.endswith("verification.k"):
        if kind in {"requires", "module", "imports", "endmodule"}:
            return "CANDIDATE_STRUCTURAL_OK", "Imports only the byte-identical supplied MPY baseline."
        notes = {
            9: (
                "CANDIDATE_DEFINITION_SOUND",
                "Total Val-to-IntSeq projection; equations at 10/11 are disjoint and exhaustive.",
            ),
            10: (
                "CANDIDATE_DEFINITION_SOUND",
                "Exact projection equation stringCodes(str(S)) = S.",
            ),
            11: (
                "CANDIDATE_DEFINITION_SOUND",
                "Owise value for non-strings; harmless because constructor inequality makes the recognizer guard false.",
            ),
            14: (
                "CANDIDATE_DEFINITION_SOUND",
                "Total structural predicate over the two ValSeq constructors.",
            ),
            15: (
                "CANDIDATE_DEFINITION_SOUND",
                "Empty sequence is a sequence of strings.",
            ),
            16: (
                "CANDIDATE_DEFINITION_SOUND",
                "Cons case recognizes a string head and recursively checks the strict tail.",
            ),
            22: (
                "CANDIDATE_DEFINITION_SOUND",
                "Partial left-fold symbol, used only under isStringSeq.",
            ),
            23: (
                "CANDIDATE_DEFINITION_SOUND",
                "Empty fold returns the accumulator.",
            ),
            24: (
                "CANDIDATE_DEFINITION_SOUND",
                "Guard forces a string head; seqConcat then appends exact head codes and recursion descends.",
            ),
            30: (
                "CANDIDATE_DEFINITION_SOUND",
                "Partial final-loop-target symbol, used only on string sequences.",
            ),
            31: (
                "CANDIDATE_DEFINITION_SOUND",
                "No remaining iteration preserves the prior loop-target value.",
            ),
            32: (
                "CANDIDATE_DEFINITION_SOUND",
                "A nonempty iteration makes the head current and recurses on the strict tail.",
            ),
            39: (
                "CANDIDATE_SIMPLIFICATION_SOUND",
                "Guard is true exactly when V=str(B); RHS then equals fixed MPY-STR applyBin and changes no cell/control state.",
            ),
        }
        return notes.get(line, ("CANDIDATE_REVIEWED_OK", "Candidate-local declaration reviewed with its attached rules."))

    if path.endswith("spec.k"):
        if kind == "claim":
            notes = {
                7: (
                    "CANDIDATE_CLAIM_PROVED_SOUND",
                    "Exact empty #loop execution; independently #Top with arbitrary continuation and framed cells.",
                ),
                40: (
                    "CANDIDATE_CLAIM_PROVED_SOUND",
                    "One real iteration plus structural recurrence; guard is exactly nonempty List[str].",
                ),
                74: (
                    "CANDIDATE_CLAIM_PROVED_SOUND",
                    "Exact regenerated Module/body/call with result and observable cells constrained.",
                ),
            }
            return notes[line]
        return "CANDIDATE_STRUCTURAL_OK", "Spec import/module structure; no semantic axiom."

    raise AssertionError(path)


def main() -> int:
    with SOURCE.open(newline="") as stream:
        rows = list(csv.DictReader(stream, dialect="excel-tab"))
    source_fieldnames = list(rows[0])
    output_rows = []
    for row in rows:
        path = row["file"]
        line = int(row["line"])
        kind = row["kind"]
        if path.startswith("/reference/reference-semantics/"):
            if fixed_is_used(path, line):
                disposition = "FIXED_USED_SOUND"
                rationale = (
                    "Reachable supplied-semantics declaration/rule; checked against the exact program path "
                    "(load, lookup, call/frame, assignment, list iteration, string append, return)."
                )
            elif kind == "rule":
                disposition = "FIXED_UNUSED_INERT"
                rationale = (
                    "Byte-identical launcher-supplied rule; its LHS construct/sort is unreachable from the "
                    "submitted program and proof summaries, so it cannot contribute to claim closure."
                )
            else:
                disposition = "FIXED_DECLARATION_OR_STRUCTURE"
                rationale = (
                    "Byte-identical launcher-supplied syntax/module structure; no candidate-local correctness axiom."
                )
        else:
            disposition, rationale = candidate_assessment(path, line, kind)
        row["disposition"] = disposition
        row["rationale"] = rationale
        output_rows.append(row)

    fieldnames = source_fieldnames + ["disposition", "rationale"]
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(output_rows)

    counts = Counter(row["disposition"] for row in output_rows)
    print(f"rows={len(output_rows)}")
    print(f"dispositions={dict(sorted(counts.items()))}")
    print(f"unassessed={sum(1 for row in output_rows if not row['disposition'])}")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
