#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory with source line ranges."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/125-split-words")
paths = [WORK / "reference-semantics" / "semantics.k"]
paths.extend(sorted((WORK / "reference-semantics" / "semantics").glob("*.k")))
paths.extend([WORK / "verification.k", WORK / "spec.k"])

anchor = re.compile(
    r'^\s*(?:requires\s+"|module\b|endmodule\b|imports\b|configuration\b|'
    r"syntax\b|rule\b|claim\b|context\b|alias\b)"
)

overall: Counter[str] = Counter()
for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if anchor.match(line)]
    print(f"\n===== {path.relative_to(WORK)} =====")
    file_counts: Counter[str] = Counter()
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        # Trailing comments/blank lines introduce the next concept, not the
        # current declaration; trim them from the displayed block.
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        if not block_lines:
            continue
        first = block_lines[0].strip()
        kind = first.split(maxsplit=1)[0]
        flags: list[str] = []
        text = "\n".join(block_lines)
        code_text = "\n".join(line.split("//", 1)[0] for line in block_lines)
        for marker, label in (
            ("[function", "function"),
            ("total", "total"),
            ("functional", "functional"),
            ("simplification", "simplification"),
            ("priority(", "priority"),
            ("owise", "owise"),
            ("concrete", "concrete"),
            ("symbolic", "symbolic"),
        ):
            if marker in code_text:
                flags.append(label)
        if kind == "syntax" and "function" in flags and "total" not in flags:
            flags.append("partial-or-opaque-function")
        label = f" [{', '.join(flags)}]" if flags else ""
        final_line = start + len(block_lines)
        print(f"\n{start + 1}-{final_line} {kind}{label}")
        for offset, line in enumerate(block_lines, start + 1):
            print(f"{offset:5d}: {line}")
        file_counts[kind] += 1
        overall[kind] += 1
        for flag in flags:
            file_counts[f"flag:{flag}"] += 1
            overall[f"flag:{flag}"] += 1
    print("\nFILE_COUNTS", dict(sorted(file_counts.items())))

print("\n===== OVERALL_COUNTS =====")
print(dict(sorted(overall.items())))
