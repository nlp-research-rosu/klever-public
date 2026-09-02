#!/usr/bin/env python3
"""Textual, line-numbered inventory of every K declaration in audit scope."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|"
    r"syntax(?:\s+priority)?|context(?:\s+alias)?|rule|claim)\b"
)
ATTRIBUTE = re.compile(
    r"\b(function|total|functional|symbol|hook|token|macro|macro-rec|"
    r"simplification|concrete|anywhere|owise|priority|preserves-definedness|"
    r"assoc|comm|idem|unit|strict|seqstrict)\b"
)


def classify(line: str) -> str:
    stripped = line.strip()
    for kind in (
        "requires",
        "endmodule",
        "imports",
        "configuration",
        "context alias",
        "context",
        "syntax priority",
        "syntax",
        "rule",
        "claim",
        "module",
    ):
        if stripped.startswith(kind):
            return kind
    return "unknown"


def normalize(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip())


def main() -> None:
    kind_counts: Counter[str] = Counter()
    attribute_counts: Counter[str] = Counter()
    total_items = 0

    for path in FILES:
        lines = path.read_text().splitlines()
        starts = [index for index, line in enumerate(lines) if START.match(line)]
        print(f"\n=== {path.relative_to(ROOT)} ({len(starts)} items) ===")
        for position, start in enumerate(starts):
            stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
            block = lines[start:stop]
            kind = classify(lines[start])
            text = normalize(block)
            attrs = sorted(set(ATTRIBUTE.findall(text)))
            kind_counts[kind] += 1
            attribute_counts.update(attrs)
            total_items += 1
            print(
                f"{path.relative_to(ROOT)}:{start + 1} "
                f"kind={kind} attrs={','.join(attrs) or '-'} :: {text}"
            )

    print("\n=== TOTALS ===")
    print(f"files={len(FILES)}")
    print(f"items={total_items}")
    print(f"kind_counts={dict(sorted(kind_counts.items()))}")
    print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")


if __name__ == "__main__":
    main()
