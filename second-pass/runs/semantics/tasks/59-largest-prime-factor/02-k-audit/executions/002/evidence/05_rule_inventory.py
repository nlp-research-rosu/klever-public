#!/usr/bin/env python3
"""Exhaustive source-level inventory of candidate K declarations and rules.

Each top-level declaration block is emitted with its complete source span.
The report includes all supplied semantics files, verification.k, and spec.k.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/candidate")
FILES = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)

START = re.compile(
    r"^\s{0,2}(module|configuration|syntax|context|rule|claim)\b"
)


def classify(block: str) -> list[str]:
    first = START.match(block.splitlines()[0])
    kinds = [first.group(1) if first else "unknown"]
    for flag in (
        "function",
        "functional",
        "total",
        "macro",
        "macro-rec",
        "no-evaluators",
        "concrete",
        "owise",
        "simplification",
        "circularity",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", block):
            kinds.append(flag)
    if "symbol(" in block:
        kinds.append("symbol")
    if "priority(" in block:
        kinds.append("priority")
    return kinds


grand = Counter()
for path in FILES:
    lines = path.read_text().splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines):
        if START.match(line) and not line.lstrip().startswith("endmodule"):
            starts.append(index)
    print(f"\n{'=' * 88}\nFILE {path}\n{'=' * 88}")
    file_counts = Counter()
    for ordinal, start in enumerate(starts, 1):
        next_start = starts[ordinal] if ordinal < len(starts) else len(lines)
        end = next_start
        while end > start and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        block = "\n".join(lines[start:end])
        flags = classify(block)
        file_counts.update(flags)
        grand.update(flags)
        print(
            f"\nDECL {ordinal:03d} lines {start + 1}-{end} "
            f"class={','.join(flags)}"
        )
        for number in range(start, end):
            print(f"{number + 1:5d} | {lines[number]}")
    print("\nFILE_COUNTS", dict(sorted(file_counts.items())))

print(f"\n{'=' * 88}\nGRAND_COUNTS\n{'=' * 88}")
for key, value in sorted(grand.items()):
    print(f"{key}: {value}")
