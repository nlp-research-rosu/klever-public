#!/usr/bin/env python3
"""Emit an exhaustive, line-addressable inventory of K declarations and rules."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/69-search")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(?P<kind>"
    r"module|endmodule|imports|requires|configuration|"
    r"syntax|rule|claim|context(?:\s+alias)?|alias"
    r")\b"
)
ATTRS = [
    "function",
    "functional",
    "total",
    "symbol",
    "macro",
    "macro-rec",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "anywhere",
    "no-evaluators",
]


def main() -> None:
    totals: Counter[str] = Counter()
    attrs: Counter[str] = Counter()
    print("INVENTORY_FORMAT: file:line | kind | complete source record")
    print(f"SOURCE_FILE_COUNT: {len(FILES)}")
    for path in FILES:
        lines = path.read_text().splitlines()
        rel = path.relative_to(ROOT)
        print(f"\nFILE {rel} lines={len(lines)}")
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = START.match(line)
            if match:
                starts.append((index, match.group("kind")))
        for pos, (index, kind) in enumerate(starts):
            next_index = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
            record_lines = lines[index:next_index]
            while record_lines and not record_lines[-1].strip():
                record_lines.pop()
            text = "\n".join(record_lines)
            totals[kind] += 1
            if kind in {"syntax", "rule", "claim", "context", "context alias", "alias"}:
                for attr in ATTRS:
                    if re.search(rf"(?<![\w-]){re.escape(attr)}(?![\w-])", text):
                        attrs[attr] += 1
            indented = "\n".join(f"    {line}" for line in record_lines)
            print(f"{rel}:{index + 1} | {kind} |\n{indented}")

    print("\nTOTALS")
    for kind, count in sorted(totals.items()):
        print(f"{kind}={count}")
    print("ATTRIBUTE_RECORD_COUNTS")
    for attr in ATTRS:
        print(f"{attr}={attrs[attr]}")
    print("INVENTORY_COMPLETE=true")


if __name__ == "__main__":
    main()
