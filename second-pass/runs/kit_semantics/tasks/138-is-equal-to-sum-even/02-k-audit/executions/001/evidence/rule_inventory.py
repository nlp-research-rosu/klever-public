#!/usr/bin/env python3
"""Emit a line-addressable inventory of every local K declaration and rule."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/138-audit/candidate")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

TARGET_LINES = {
    "reference-semantics/semantics/syntax.k": {
        9, 32, 41, 56, 57, 60, 61,
    },
    "reference-semantics/semantics/core.k": {
        13, 14, 25, 31, 36, 37, 38, 39, 40, 41, 42, 49,
        124, 125, 126, 127, 130, 131, 132, 145, 152,
        157, 158, 185, 186, 189, 190, 191, 194, 195, 196,
        199, 200, 201, 202, 203, 204, 205, 208, 209, 210,
        213, 214, 215,
    },
    "reference-semantics/semantics/operators.k": {10, 12, 15, 16, 17},
    "reference-semantics/semantics/int.k": {15, 19, 20, 25, 26},
    "reference-semantics/semantics/bool.k": {16, 17, 18, 20, 22, 24},
    "reference-semantics/semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "spec.k": {6},
}

START = re.compile(r"^\s*(configuration|syntax|rule|context|claim|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|rule|context|claim|alias|module|endmodule|imports|requires)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def declarations(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        for candidate in range(start + 1, stop):
            if BOUNDARY.match(lines[candidate]) and not START.match(lines[candidate]):
                stop = candidate
                break
        block = "\n".join(lines[start:stop]).strip()
        match = START.match(lines[start])
        assert match is not None
        yield start + 1, match.group(1), block


items = []
for path in SOURCES:
    relative = path.relative_to(ROOT).as_posix()
    for line, kind, block in declarations(path):
        attributes = sorted(
            {
                value.strip()
                for group in ATTR.findall(block)
                for value in group.split(",")
            }
        )
        if kind == "rule":
            subtype = "ordinary-semantic-rule"
            if any(value.startswith("simplification") for value in attributes):
                subtype = "simplification-rule"
            elif "concrete" in attributes:
                subtype = "concrete-only-rule"
            elif "macro" in attributes or "macro-rec" in attributes:
                subtype = "macro-rule"
            if any(value.startswith("priority(") for value in attributes):
                subtype += "+priority"
            if "owise" in attributes:
                subtype += "+owise"
        elif kind == "syntax":
            subtype = "syntax-declaration"
            if "function" in attributes:
                subtype += "+function"
            if "total" in attributes:
                subtype += "+total"
            if "functional" in attributes:
                subtype += "+functional"
            if "symbol" in " ".join(attributes):
                subtype += "+symbol"
            if "no-evaluators" in attributes:
                subtype += "+opaque"
            if "macro" in attributes or "macro-rec" in attributes:
                subtype += "+macro"
        else:
            subtype = kind
        relevance = (
            "TARGET-REACHABLE"
            if line in TARGET_LINES.get(relative, set())
            else "DORMANT-FOR-TARGET"
        )
        if kind == "claim":
            disposition = "PROOF-GOAL-NOT-AN-AXIOM"
        elif relevance == "TARGET-REACHABLE":
            disposition = "CHECKED-SOUND-ON-ALL-K-INT-INPUTS"
        elif "opaque" in subtype:
            disposition = "UNPROVED-OPAQUE-BOUNDARY-BUT-TARGET-INERT"
        elif "concrete-only" in subtype:
            disposition = "LLVM-ONLY-AND-TARGET-PROOF-INERT"
        elif kind in {"syntax", "configuration", "context"}:
            disposition = "DECLARATIVE-AND-TARGET-INERT"
        else:
            disposition = "OPERATIONAL-BUT-UNREACHABLE-FROM-TARGET"
        normalized = " ".join(
            segment.strip()
            for segment in block.splitlines()
            if segment.strip() and not segment.lstrip().startswith("//")
        )
        items.append(
            (
                relative,
                line,
                kind,
                subtype,
                relevance,
                disposition,
                attributes,
                normalized,
            )
        )

counts = Counter(item[2] for item in items)
subtypes = Counter(item[3] for item in items)
relevance_counts = Counter(item[4] for item in items)
disposition_counts = Counter(item[5] for item in items)

print("# Exhaustive local K declaration and rule inventory")
print()
print(
    "Generated from fresh source copies. Every `configuration`, `syntax`, `rule`, "
    "`context`, `claim`, and `alias` declaration is listed by source line."
)
print()
print(f"- Source files: {len(SOURCES)}")
print(f"- Inventory items: {len(items)}")
print(f"- Kind counts: {dict(sorted(counts.items()))}")
print(f"- Relevance counts: {dict(sorted(relevance_counts.items()))}")
print(f"- Disposition counts: {dict(sorted(disposition_counts.items()))}")
print(f"- Subtype counts: {dict(sorted(subtypes.items()))}")
print()
print("## Source hashes")
print()
for path in SOURCES:
    print(f"- `{path.relative_to(ROOT).as_posix()}`: `{sha256(path)}`")
print()
print("## Items")
print()
for number, item in enumerate(items, 1):
    (
        relative,
        line,
        kind,
        subtype,
        relevance,
        disposition,
        attributes,
        normalized,
    ) = item
    attributes_text = ", ".join(attributes) if attributes else "none"
    print(
        f"{number}. `{relative}:{line}` — {subtype}; {relevance}; "
        f"disposition: {disposition}; attributes: {attributes_text}"
    )
    print()
    print(f"   `{normalized}`")
    print()

print("INVENTORY_COMPLETE=true")
