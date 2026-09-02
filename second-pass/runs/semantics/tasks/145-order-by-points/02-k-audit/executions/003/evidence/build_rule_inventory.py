#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule inventory.

Items include modules/imports, configuration, syntax declarations, contexts,
rules, claims, and their continuation lines (guards/attributes/cells). This is
an inventory, not an automated soundness verdict.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/source/reference-semantics")
paths = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
paths.append(Path("/tmp/audit-work/source/verification.k"))

def is_item_start(line: str) -> bool:
    return (
        line.startswith("requires ")
        or line.startswith("module ")
        or line.startswith("endmodule")
        or line.startswith("  imports ")
        or line.startswith("  configuration")
        or line.startswith("  syntax ")
        or line.startswith("  context ")
        or line.startswith("  rule ")
        or line.startswith("  claim ")
    )


def kind(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("syntax "):
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "macro",
        ):
            if attr in stripped:
                attrs.append(attr)
        return "syntax" + (":" + ",".join(attrs) if attrs else "")
    return stripped.split(maxsplit=1)[0] if stripped else "blank"


overall = Counter()
print("# Exhaustive K source inventory")
print()
print("Source: clean scratch copy; line numbers are within each named file.")
print()
for path in paths:
    relative = (
        str(path.relative_to(ROOT))
        if path.is_relative_to(ROOT)
        else path.name
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if is_item_start(line)]
    file_counts = Counter()
    items = []
    for position, start in enumerate(starts):
        end_limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
        start_kind = kind(lines[start])
        if start_kind in {"module", "endmodule", "imports", "requires"}:
            end = start + 1
        else:
            end = end_limit
            while end > start + 1 and not lines[end - 1].strip():
                end -= 1
            while end > start + 1 and lines[end - 1].lstrip().startswith("//"):
                end -= 1
        text = "\n".join(lines[start:end])
        items.append((start + 1, end, start_kind, text))
        base_kind = start_kind.split(":", 1)[0]
        file_counts[base_kind] += 1
        overall[base_kind] += 1

    print(f"## `{relative}`")
    print()
    print(
        "Counts: "
        + ", ".join(f"{name}={count}" for name, count in sorted(file_counts.items()))
    )
    print()
    for start, end, item_kind, text in items:
        attrs = []
        lowered = text.lower()
        for marker in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "macro",
        ):
            if marker in lowered:
                attrs.append(marker)
        print(
            f"- lines {start}-{end}; kind `{item_kind}`; "
            f"markers `{','.join(attrs) if attrs else 'none'}`"
        )
        print()
        print("  ```k")
        for line in text.splitlines():
            print("  " + line)
        print("  ```")
        print()

print("## Overall counts")
print()
for name, count in sorted(overall.items()):
    print(f"- {name}: {count}")
