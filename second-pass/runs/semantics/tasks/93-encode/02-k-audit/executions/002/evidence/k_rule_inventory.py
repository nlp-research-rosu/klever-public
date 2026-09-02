#!/usr/bin/env python3
"""Emit a stable, line-addressed inventory of K declarations and rules."""

from __future__ import annotations

import re
import sys
from pathlib import Path


START = re.compile(r"^\s*(syntax|rule|claim|configuration|context)\b")
STOP = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|module|endmodule|imports|requires)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "concrete",
    "priority",
    "macro",
    "macro-rec",
    "simplification",
    "anywhere",
    "owise",
    "strict",
    "seqstrict",
)


def clean(block: list[str]) -> str:
    without_comments = [line.split("//", 1)[0].strip() for line in block]
    return " ".join(" ".join(without_comments).split())


def inventory(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    records: list[str] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines) and not STOP.match(lines[index]):
            index += 1
        block = clean(lines[start:index])
        tags = [
            attr
            for attr in ATTRS
            if re.search(rf"(?<![-\w]){re.escape(attr)}(?![-\w])", block)
        ]
        end = index
        records.append(
            f"{path}:{start + 1}-{end} | {match.group(1)}"
            f" | attrs={','.join(tags) if tags else '-'} | {block}"
        )
    return records


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: k_rule_inventory.py FILE...", file=sys.stderr)
        return 2
    total = 0
    for raw_path in sys.argv[1:]:
        path = Path(raw_path)
        records = inventory(path)
        print(f"FILE {path} RECORDS {len(records)}")
        for record in records:
            print(record)
        total += len(records)
    print(f"TOTAL_RECORDS {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
