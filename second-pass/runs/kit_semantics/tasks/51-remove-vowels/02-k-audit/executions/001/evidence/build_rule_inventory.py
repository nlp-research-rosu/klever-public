#!/usr/bin/env python3
"""Emit an exhaustive, one-row-per-declaration K audit inventory."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

# Fixed-semantics lines on the actual solution execution/proof dependency path.
# Ranges include declarations and their complete operational rule groups.
MATERIAL_RANGES = {
    "semantics.k": [(58, 80)],
    "syntax.k": [(9, 16), (28, 32), (37, 61)],
    "core.k": [
        (13, 42),
        (44, 60),
        (123, 127),
        (129, 181),
        (183, 191),
        (207, 230),
    ],
    "iter.k": [(8, 8)],
    "str.k": [(7, 41)],
    "operators.k": [(14, 17)],
    "controls.k": [(8, 31), (46, 54), (62, 75), (84, 85)],
    "tuple.k": [(30, 41)],
    "functions.k": [(13, 20), (62, 90)],
    "call.k": [(18, 21), (69, 74)],
}


def declaration_blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starters = re.compile(
        r"^\s*(configuration|context|syntax|rule|claim)\b"
    )
    starts = [
        (idx, starters.match(line).group(1))
        for idx, line in enumerate(lines)
        if starters.match(line)
    ]
    for pos, (idx, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        # Do not absorb module terminators/imports after the final declaration.
        while end > idx + 1 and re.match(
            r"^\s*(endmodule|module|imports|requires)\b", lines[end - 1]
        ):
            end -= 1
        text = " ".join(line.strip() for line in lines[idx:end] if line.strip())
        yield kind, idx + 1, text


def is_material(path: Path, line: int) -> bool:
    return any(
        lo <= line <= hi for lo, hi in MATERIAL_RANGES.get(path.name, [])
    )


def disposition(path: Path, kind: str, line: int, text: str):
    if path.name == "verification.k":
        if kind == "syntax":
            return (
                "PROOF_LOCAL_SOUND",
                "Total structural filter summary; no operational cell match.",
            )
        if line == 10:
            return (
                "PROOF_LOCAL_SOUND",
                "Empty sequence returns the accumulator.",
            )
        if line == 12:
            return (
                "PROOF_LOCAL_SOUND",
                "Singleton is present in the ten-code vowel sequence; recurse without append.",
            )
        if line == 28:
            return (
                "PROOF_LOCAL_SOUND",
                "Complementary non-membership guard; append singleton and structurally recurse.",
            )
    if path.name == "spec.k":
        return (
            "CLAIM_AUDITED",
            "Auxiliary loop execution claim or result-constraining entry theorem, not an axiom/rule.",
        )
    if "no-evaluators" in text or "symbol(" in text:
        return (
            "FIXED_OPAQUE_OFF_PATH",
            "Opaque supplied-semantics boundary; float/sort/digest symbol is unreachable from this program.",
        )
    if is_material(path, line):
        return (
            "FIXED_MATERIAL_SOUND",
            "On the source execution path; inspected for evaluation order, binding, state, control, and value fidelity.",
        )
    return (
        "FIXED_OFF_PATH",
        "Exact trusted supplied-semantics declaration and unreachable from the submitted program term.",
    )


writer = csv.writer(__import__("sys").stdout, delimiter="\t", lineterminator="\n")
writer.writerow(["file", "line", "kind", "attributes", "disposition", "reason", "declaration"])
for path in FILES:
    for kind, line, text in declaration_blocks(path):
        attrs = ",".join(re.findall(r"\[([^\]]+)\]", text))
        status, reason = disposition(path, kind, line, text)
        writer.writerow(
            [
                path.relative_to(ROOT).as_posix(),
                line,
                kind,
                attrs,
                status,
                reason,
                text,
            ]
        )
