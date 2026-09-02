#!/usr/bin/env python3
"""Exhaustive line-level inventory of the mounted K source theory."""

from __future__ import annotations

import collections
from pathlib import Path


ROOT = Path("/tmp/audit-work/45-triangle-area")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]


def classify(line: str) -> list[str]:
    stripped = line.strip()
    tags: list[str] = []
    starters = {
        "module ": "module",
        "endmodule": "endmodule",
        "imports ": "import",
        "requires ": "requires-file-or-guard",
        "ensures ": "ensures",
        "configuration ": "configuration",
        "syntax ": "syntax",
        "rule ": "rule",
        "claim ": "claim",
        "context ": "context",
        "macro ": "macro",
    }
    for prefix, tag in starters.items():
        if stripped.startswith(prefix):
            tags.append(tag)
    if stripped.startswith("|") or stripped.startswith(">"):
        tags.append("syntax-continuation")
    attributes = {
        "[function": "function-declaration",
        "function]": "function-declaration",
        "functional": "functional",
        "total": "total",
        "no-evaluators": "opaque-no-evaluators",
        "symbol(": "symbol",
        "priority(": "priority",
        "simplification": "simplification",
        "concrete": "concrete",
        "macro": "macro-attribute",
        "strict": "evaluation-order",
    }
    for needle, tag in attributes.items():
        if needle in stripped and tag not in tags:
            tags.append(tag)
    if not tags:
        tags.append("continuation")
    return tags


def main() -> int:
    totals: collections.Counter[str] = collections.Counter()
    for path in FILES:
        relative = path.relative_to(ROOT)
        lines = path.read_text().splitlines()
        file_totals: collections.Counter[str] = collections.Counter()
        inventory: list[tuple[int, list[str], str]] = []
        in_block_comment = False
        for line_number, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("/*"):
                in_block_comment = True
            is_comment = in_block_comment or not stripped or stripped.startswith("//")
            if not is_comment:
                tags = classify(line)
                inventory.append((line_number, tags, line.rstrip()))
                file_totals.update(tags)
                totals.update(tags)
            if "*/" in stripped:
                in_block_comment = False
        print(f"===== {relative} =====")
        print(
            "counts "
            + " ".join(f"{key}={value}" for key, value in sorted(file_totals.items()))
        )
        for line_number, tags, line in inventory:
            print(f"{line_number:04d} [{','.join(tags)}] {line}")
    print("===== GLOBAL COUNTS =====")
    print(" ".join(f"{key}={value}" for key, value in sorted(totals.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
