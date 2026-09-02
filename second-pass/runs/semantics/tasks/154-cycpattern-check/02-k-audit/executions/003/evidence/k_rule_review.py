#!/usr/bin/env python3
"""Per-declaration audit disposition for the exhaustive lexical K inventory."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "/audit-output/evidence")
from k_inventory import FILES, ROOT, blocks  # noqa: E402


USED_FIXED_RULES: dict[str, set[int]] = {
    "reference-semantics/semantics/core.k": {
        125, 126, 127, 131, 132, 158, 189, 190, 191, 194, 195, 200,
    },
    "reference-semantics/semantics/operators.k": {12, 17},
    "reference-semantics/semantics/str.k": {
        8, 9, 14, 15, 21, 22, 24, 29, 33, 34, 35, 38, 39, 40,
    },
    "reference-semantics/semantics/controls.k": {
        9, 52, 53, 54, 69, 71, 72, 73, 85,
    },
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 80, 85},
    "reference-semantics/semantics/call.k": {20, 21, 69},
    "reference-semantics/semantics/tuple.k": {32},
}

DISPLACED_SLICE_RULES = {
    50, 51, 52, 54, 55, 56, 61, 63, 64, 66, 68, 72, 73, 74, 76, 77,
    79, 81, 83, 84, 86, 88, 90, 91, 93, 96, 97, 99, 102, 103, 105,
    109, 110, 113, 116, 117, 120,
}


def disposition(relative: str, line: int, kind: str) -> tuple[str, str]:
    if relative == "verification.k":
        return {
            8: ("ACCEPTED_DERIVED", "symbolic true branch; agrees with fixed true rule"),
            10: ("ACCEPTED_DERIVED", "symbolic false branch; guard is disjoint from true"),
            16: ("ACCEPTED_DEFINITION", "dropOne empty equation"),
            17: ("ACCEPTED_DEFINITION", "dropOne constructor equation; structurally descends"),
            19: (
                "SOUND_EVIDENCE_GAP",
                "pure s[1:] bridge; ground checks close, universal bridge-free proof stuck",
            ),
            32: ("ACCEPTED_DEFINITION", "empty remaining iterator returns false"),
            34: ("ACCEPTED_DEFINITION", "nonempty iterator and current match returns true"),
            37: (
                "ACCEPTED_DEFINITION",
                "failed match rotates by current character and descends on remaining tail",
            ),
            51: (
                "ACCEPTED_PROVEN_BRIDGE",
                "exact complete context is the separately closed SPEC-LEMMA claim",
            ),
        }.get(line, ("DECLARATION_OK", "proof-local declaration"))

    if relative == "spec.k":
        if line == 6:
            return (
                "CLAIM_SOUND",
                "exact loop/control/frame summary; independently closes bridge-free of its promotion",
            )
        if line == 54:
            return (
                "CLAIM_INADEQUATE",
                "pins generated body but summary disagrees with source contract for empty b",
            )
        return ("DECLARATION_OK", "spec declaration")

    if kind in {"configuration", "syntax", "context"}:
        if relative == "reference-semantics/semantics/syntax.k":
            return ("FIXED_DECLARATION_USED", "declares submitted program constructors/evaluation attributes")
        if relative.endswith(("core.k", "operators.k", "subscript.k")):
            return ("FIXED_DECLARATION_REVIEWED", "fixed declaration; relevant or imported by the proof slice")
        return ("FIXED_DECLARATION_INERT", "fixed declaration not selected by submitted program terms")

    if kind == "rule":
        if line in USED_FIXED_RULES.get(relative, set()):
            return (
                "FIXED_USED_SOUND",
                "selected by actual program/claim; preserves Python binding, order, control, or string value",
            )
        if (
            relative == "reference-semantics/semantics/subscript.k"
            and line in DISPLACED_SLICE_RULES
        ):
            return (
                "FIXED_DISPLACED_REVIEWED",
                "part of fixed slice execution displaced only by proof-local s[1:] bridge",
            )
        if relative == "reference-semantics/semantics/concrete.k":
            return (
                "LLVM_ONLY_INERT",
                "only in MPY-KRUN and does not match the submitted string-only concrete harness path",
            )
        return (
            "FIXED_UNREACHABLE",
            "constructor/operator/call shape cannot arise in either submitted proof claim",
        )

    return ("ASSEMBLY_ONLY", "module/import/assembly declaration")


def main() -> int:
    print("file\tline\tkind\tstatus\treason\tdeclaration")
    count = 0
    for path in FILES:
        relative = path.relative_to(ROOT).as_posix()
        for line, kind, text in blocks(path):
            status, reason = disposition(relative, line, kind)
            escaped = text.replace("\t", " ").replace("\n", " ")
            print(f"{relative}\t{line}\t{kind}\t{status}\t{reason}\t{escaped}")
            count += 1
    print(f"# REVIEWED_DECLARATION_COUNT={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
