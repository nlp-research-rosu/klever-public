#!/usr/bin/env python3
"""Produce a source-level inventory of every local K declaration and rule."""

from __future__ import annotations

import collections
import re
from pathlib import Path

ROOT = Path("/candidate")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
INTERESTING = {"configuration", "syntax", "context", "rule", "claim"}


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0].rstrip()


records: list[tuple[Path, int, int, str, str]] = []
counts: collections.Counter[tuple[str, str]] = collections.Counter()

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(strip_comments(line))
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        if kind not in INTERESTING:
            continue
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:next_start]
        while block_lines and not strip_comments(block_lines[-1]).strip():
            block_lines.pop()
        end = start + len(block_lines)
        block = " ".join(
            piece.strip()
            for piece in map(strip_comments, block_lines)
            if piece.strip()
        )
        records.append((path, start + 1, end, kind, block))
        counts[(str(path.relative_to(ROOT)), kind)] += 1

material_fixed_files = {
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/iter.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/list.k",
    "reference-semantics/semantics/tuple.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/call.k",
    "reference-semantics/semantics/str.k",
    "reference-semantics/semantics/syntax.k",
}


def decision(path: str, start: int, kind: str) -> str:
    if path.startswith("reference-semantics/"):
        if path in material_fixed_files:
            return "FIXED_MATERIAL_REVIEWED_NO_TARGET_SLICE_DEFECT"
        return "FIXED_UNUSED_BY_TARGET_NO_PROOF_DEPENDENCE"
    if path == "spec.k":
        return "ADEQUATE_TARGET_CLAIM_BUT_CLOSES_VIA_REJECTED_BRIDGE"
    if path == "verification.k":
        if start == 74:
            return "UNSOUND_OPERATIONAL_BRIDGE_CELL_STATE_WITNESS"
        if start in {9, 14, 23, 34} and kind == "syntax":
            return "INCOMPLETE_TOTALITY_OUTSIDE_GUARDED_INTEGER_LIST_USE"
        if start in {45, 46}:
            return "EXACT_PROGRAM_PINNING_MACRO"
        return "SOUND_DEFINITIONAL_DECLARATION_OR_EQUATION_ON_MATCH_DOMAIN"
    return "UNCLASSIFIED"


print("record_id\tfile\tlines\tkind\tattributes\tdecision\tdeclaration")
for record_id, (path, start, end, kind, block) in enumerate(records, 1):
    raw_attributes = re.findall(r"\[([^\]]+)\]", block)
    attributes = ",".join(
        value
        for value in raw_attributes
        if "<-" not in value
        and re.search(
            r"\b(function|total|functional|concrete|simplification|priority|"
            r"owise|macro|strict|seqstrict|symbol|no-evaluators|hook)\b",
            value,
        )
    ).replace("\t", " ")
    declaration = re.sub(r"\s+", " ", block).replace("\t", " ")
    relative = str(path.relative_to(ROOT))
    print(
        f"K{record_id:04d}\t{relative}\t{start}-{end}\t"
        f"{kind}\t{attributes}\t{decision(relative, start, kind)}\t{declaration}"
    )

print("\nSUMMARY")
for (path, kind), count in sorted(counts.items()):
    print(f"{path}\t{kind}\t{count}")
print(f"TOTAL_RECORDS\t{len(records)}")
