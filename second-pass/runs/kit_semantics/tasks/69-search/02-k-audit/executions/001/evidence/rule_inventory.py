#!/usr/bin/env python3
"""Produce a source-complete inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|module|endmodule|imports)\b"
)

path_relevant = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/iter.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/list.k",
    "reference-semantics/semantics/tuple.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/call.k",
}


def entries(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    result = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            if not lines[index].strip():
                index += 1
                break
            index += 1
        block = "\n".join(lines[start:index]).strip()
        result.append((start + 1, kind, block))
    return result


inventory = []
counts = collections.Counter()
tag_counts = collections.Counter()
for path in FILES:
    relative = str(path.relative_to(ROOT))
    for line, kind, block in entries(path):
        tags = []
        for tag, pattern in [
            ("function", r"\bfunction\b"),
            ("total", r"\btotal\b"),
            ("functional", r"\bfunctional\b"),
            ("opaque/no-evaluators", r"\bno-evaluators\b"),
            ("priority", r"\bpriority\s*\("),
            ("simplification", r"\bsimplification\b"),
            ("concrete", r"\bconcrete\b"),
            ("owise", r"\bowise\b"),
            ("macro", r"\bmacro(?:-rec)?\b"),
            ("strict", r"\b(?:seq)?strict\b"),
            ("symbol", r"\bsymbol\s*\("),
            ("preserves-definedness", r"\bpreserves-definedness\b"),
        ]:
            if re.search(pattern, block):
                tags.append(tag)
                tag_counts[tag] += 1
        if relative == "verification.k":
            assessment = "candidate proof extension; individually audited in REVIEW.md"
        elif relative == "spec.k":
            assessment = "candidate reachability claim; adequacy audited in REVIEW.md"
        elif relative in path_relevant:
            assessment = "trusted supplied baseline; contains rules on the submitted path"
        else:
            assessment = "trusted supplied baseline; no construct from solution.mpy reaches this entry"
        compact = " ".join(piece.strip() for piece in block.splitlines())
        inventory.append((relative, line, kind, ",".join(tags) or "-", assessment, compact))
        counts[kind] += 1

print("# Exhaustive K declaration and rule inventory")
print()
print("Generated from the fresh source-only scratch tree.")
print()
print("## Counts")
print()
print("| Kind | Count |")
print("|---|---:|")
for kind in ["configuration", "syntax", "context", "rule", "claim"]:
    print(f"| {kind} | {counts[kind]} |")
print()
print("| Attribute/tag | Entries |")
print("|---|---:|")
required_tags = [
    "function",
    "total",
    "functional",
    "opaque/no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "strict",
    "symbol",
    "preserves-definedness",
]
for tag in required_tags:
    print(f"| {tag} | {tag_counts[tag]} |")
print()
print("## Entries")
print()
print("| Source | Line | Kind | Attributes | Assessment class | Complete source block |")
print("|---|---:|---|---|---|---|")
for relative, line, kind, tags, assessment, compact in inventory:
    escaped = compact.replace("|", "&#124;").replace("`", "&#96;")
    print(
        f"| `{relative}` | {line} | {kind} | {tags} | {assessment} | {escaped} |"
    )
