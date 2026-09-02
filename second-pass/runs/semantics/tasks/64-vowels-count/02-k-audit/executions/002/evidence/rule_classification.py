#!/usr/bin/env python3
"""Per-rule relevance and soundness classification for the audited theorem."""

from __future__ import annotations

import pathlib
import re
from collections import Counter


ROOT = pathlib.Path("/tmp/audit-work/proof")
PATHS = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k"]
)

# Rules reached either by the entry theorem or its bridge-free loop connection
# theorem. Syntax strictness/contexts are mapped separately in REVIEW.md.
USED_FIXED: dict[str, set[int]] = {
    "reference-semantics/semantics/core.k": {
        125, 126, 127, 131, 132, 158, 189, 190, 191, 194, 195,
        200, 214, 215,
    },
    "reference-semantics/semantics/str.k": {
        8, 9, 14, 15, 16, 29, 33, 34, 35, 38, 39, 40,
    },
    "reference-semantics/semantics/methods.k": {
        19, 113, 142, 143, 155, 156,
    },
    "reference-semantics/semantics/operators.k": {12, 17},
    "reference-semantics/semantics/int.k": {9, 11},
    "reference-semantics/semantics/controls.k": {
        9, 20, 52, 53, 54, 69, 71, 72, 73,
    },
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 85},
    "reference-semantics/semantics/call.k": {16, 20, 21, 24, 69},
    "reference-semantics/semantics/tuple.k": {32},
}

UNICODE_DEFECT = {
    ("reference-semantics/semantics/methods.k", 19),
    ("reference-semantics/semantics/methods.k", 143),
    ("reference-semantics/semantics/methods.k", 156),
}

LOCAL_SOUND = {
    8, 12, 13, 24, 25, 34, 35, 39, 45, 58, 68,
}


def first_line(text: str) -> str:
    return " ".join(text.strip().split())[:260]


def main() -> int:
    results: list[tuple[str, int, str, str, str]] = []
    totals: Counter[str] = Counter()

    for path in PATHS:
        rel = path.relative_to(ROOT).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        rule_starts = [
            index
            for index, line in enumerate(lines)
            if re.match(r"^\s*rule\b", line)
        ]
        declaration_starts = [
            index
            for index, line in enumerate(lines)
            if re.match(
                r"^\s*(rule|syntax(?:\s+priority)?|claim|configuration|"
                r"context(?:\s+alias)?|module|endmodule|imports)\b",
                line,
            )
            or re.match(r'^requires\s+"', line)
        ]
        for start in rule_starts:
            later = [index for index in declaration_starts if index > start]
            end = min(later) if later else len(lines)
            block = "\n".join(lines[start:end])
            line_no = start + 1

            if rel == "verification.k":
                if line_no == 78:
                    classification = "UNSOUND_OPERATIONAL_BRIDGE"
                    rationale = (
                        "Bridge omits env/scopeLoc/ret/exc/exit and therefore "
                        "matches states outside its bridge-free theorem; the "
                        "env=0 witness proves a false scope-1 update."
                    )
                elif line_no in LOCAL_SOUND:
                    classification = "SOUND_PROOF_LOCAL"
                    rationale = (
                        "Truthful structural equation or exact constructor "
                        "macro; recursive equations cover constructors and "
                        "decrease, and expanded program KORE was identical."
                    )
                else:
                    classification = "LOCAL_REVIEW_GAP"
                    rationale = "Unexpected local rule; review manually."
            elif (rel, line_no) in UNICODE_DEFECT:
                classification = "UNSOUND_REAL_PYTHON_UNICODE"
                rationale = (
                    "For input iCons(304,.IntSeq), modeled lower keeps 304 and "
                    "the theorem returns 0, while submitted CPython lower maps "
                    "U+0130 to i+combining-dot and the program returns 1."
                )
            elif line_no in USED_FIXED.get(rel, set()):
                classification = "SOUND_ON_USED_ASCII_SLICE"
                rationale = (
                    "Reached by the program/connection theorem; rule follows "
                    "the relevant constructor, evaluation-order, scope, or "
                    "ASCII string behavior. Unicode lower is classified "
                    "separately."
                )
            else:
                classification = "INERT_FOR_THIS_THEOREM"
                rationale = (
                    "Rule head cannot arise from the submitted constructors or "
                    "their reached continuations. Read in the exhaustive source "
                    "review; no global soundness claim is made without a "
                    "witness, and it contributes nothing to claim closure."
                )

            totals[classification] += 1
            results.append(
                (rel, line_no, classification, rationale, first_line(block))
            )

    print("SUMMARY")
    for classification in sorted(totals):
        print(f"{classification}\t{totals[classification]}")
    print(f"TOTAL_RULES\t{len(results)}")
    print("\nRULES")
    for number, (path, line, classification, rationale, source) in enumerate(
        results, 1
    ):
        print(
            f"{number:04d}\t{path}:{line}\t{classification}\t"
            f"{rationale}\t{source}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
