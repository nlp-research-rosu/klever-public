#!/usr/bin/env python3
"""Lexical, source-located inventory of K declarations, rules, and claims."""

from __future__ import annotations

import re
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/verification.k"),
    Path("/tmp/audit-work/spec.k"),
]

START = re.compile(
    r"^\s*(configuration\b|syntax\b|context\b|rule\b|claim\b|priority\b)"
)


def records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        # Stop at a module delimiter or blank-separated comment after the item.
        body = []
        for index in range(start, stop):
            line = lines[index]
            if index > start and re.match(r"^\s*(end)?module\b", line):
                break
            body.append(line)
        yield start + 1, "\n".join(body).rstrip()


def main() -> None:
    counts: dict[str, int] = {}
    total = 0
    for path in ROOTS:
        print(f"FILE {path}")
        file_count = 0
        for line_number, body in records(path):
            first = body.lstrip().split(None, 1)[0]
            counts[first] = counts.get(first, 0) + 1
            total += 1
            file_count += 1
            print(f"ITEM {path}:{line_number}")
            print(body)
        print(f"FILE_ITEM_COUNT {file_count}")
    print(f"TOTAL_ITEMS {total}")
    print(f"KIND_COUNTS {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
