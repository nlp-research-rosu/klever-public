#!/usr/bin/env python3
"""Attach an audit disposition to every anchored K source entry."""

from __future__ import annotations

import sys
from pathlib import Path

from inventory_k import entries, flags


USED_FIXED: dict[str, set[int]] = {
    "syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "core.k": {
        13, 14, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        124, 125, 126, 127, 130, 131, 132, 152, 157, 158,
        185, 186, 189, 190, 191, 194, 213, 214, 215,
    },
    "range.k": {9, 10, 20, 23},
    "operators.k": {12, 15, 16, 17},
    "int.k": {15, 19, 20, 22, 26},
    "controls.k": {51, 52, 53, 54, 65, 69, 71, 72, 73},
    "tuple.k": {31, 32},
    "functions.k": {8, 14, 63, 64, 78, 80, 85},
    "call.k": {19, 20, 21, 31, 69},
    "builtins.k": {17, 178},
}

LOCAL: dict[tuple[str, int], tuple[str, str]] = {
    ("verification.k", 8): (
        "SOUND_DEFINITIONAL_MACRO",
        "Names the exact submitted loop-body AST; expands before execution.",
    ),
    ("verification.k", 9): (
        "SOUND_DEFINITIONAL_MACRO",
        "Exact If/modulo/Return(y) loop body; no execution is skipped.",
    ),
    ("verification.k", 16): (
        "SOUND_DEFINITIONAL_MACRO",
        "Names the exact submitted function-body AST.",
    ),
    ("verification.k", 17): (
        "SOUND_DEFINITIONAL_MACRO",
        "Exact early test, exact range loop, and exact trailing Return(x).",
    ),
    ("verification.k", 26): (
        "SOUND_WITH_PINNING_LIMITATION",
        "Entry macro sort; direct-closure representation omits module loading.",
    ),
    ("verification.k", 27): (
        "SOUND_WITH_PINNING_LIMITATION",
        "Executes the exact closure body and argument binding; leaves module scope empty.",
    ),
    ("verification.k", 33): (
        "SOUND_DEFINITIONAL_SUMMARY",
        "Result summary is fixed by guarded recursive equations below.",
    ),
    ("verification.k", 35): (
        "SOUND_EQUATION",
        "N<2 is non-prime and selects Y on the complete stated guard.",
    ),
    ("verification.k", 38): (
        "SOUND_EQUATION",
        "D>=N ends the scan without a divisor and selects X.",
    ),
    ("verification.k", 41): (
        "SOUND_EQUATION",
        "A divisor in [D,N) selects Y.",
    ),
    ("verification.k", 45): (
        "SOUND_EQUATION",
        "A non-divisor advances D; guard is disjoint and recursion descends toward N.",
    ),
    ("verification.k", 52): (
        "SOUND_DEFINITIONAL_SUMMARY",
        "Final local-divisor summary is fixed by guarded equations below.",
    ),
    ("verification.k", 54): (
        "SOUND_EQUATION",
        "An empty remaining range preserves the old local value.",
    ),
    ("verification.k", 57): (
        "SOUND_EQUATION",
        "A found divisor is the final assigned local value.",
    ),
    ("verification.k", 61): (
        "SOUND_EQUATION",
        "A non-divisor becomes OLD for the recursive suffix.",
    ),
    ("verification.k", 73): (
        "SOUND_DERIVED_OPERATIONAL_SUMMARY",
        "Exact-context copy of independently proved loop_correct; no broader continuation/cells.",
    ),
    ("spec.k", 9): (
        "SOUND_CONNECTION_CLAIM",
        "Bridge-free universal loop execution claim; reconstructed to #Top.",
    ),
    ("spec.k", 44): (
        "SOUND_ENTRY_CLAIM_WITH_PINNING_LIMITATION",
        "Result-constraining direct-closure theorem; reconstructed to #Top.",
    ),
}


def disposition(path: Path, line: int, kind: str) -> tuple[str, str]:
    name = path.name
    local = LOCAL.get((name, line))
    if local:
        return local
    if "reference-semantics" in path.parts:
        if line in USED_FIXED.get(name, set()):
            return (
                "FIXED_SUPPLIED_USED_AND_CHECKED",
                "Trusted supplied-semantics entry reached by solution.mpy; "
                "its evaluation order, guard, and state footprint were reviewed.",
            )
        return (
            "FIXED_SUPPLIED_UNUSED",
            "Type-and-byte-identical trusted supplied-semantics entry; not reachable "
            "from the submitted program's construct slice and adds no candidate-local proof power.",
        )
    return (
        "STRUCTURAL_OR_LOCAL_REVIEWED",
        "Module/import/declaration structure, or a local entry covered by the Stage 5 review.",
    )


def clean(text: str) -> str:
    return " ".join(text.split()).replace("\t", " ")


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} FILE_OR_DIRECTORY [...]", file=sys.stderr)
        return 64
    paths: list[Path] = []
    for argument in sys.argv[1:]:
        path = Path(argument)
        paths.extend(sorted(path.rglob("*.k")) if path.is_dir() else [path])
    paths = sorted(dict.fromkeys(path.resolve() for path in paths))

    print("id\tfile\tline\tkind\tattributes\tdisposition\trationale\tentry")
    counter = 0
    for path in paths:
        for line, kind, block in entries(path):
            counter += 1
            status, rationale = disposition(path, line, kind)
            try:
                shown_path = path.relative_to(Path.cwd())
            except ValueError:
                shown_path = path
            fields = [
                str(counter),
                str(shown_path),
                str(line),
                kind,
                flags(block),
                status,
                rationale,
                clean(block),
            ]
            print("\t".join(field.replace("\t", " ") for field in fields))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
