#!/usr/bin/env python3
"""Summarize the exhaustive K inventory by file and sensitive attribute."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


FILES = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/reconstruction/verification.k"),
    Path("/tmp/audit-work/reconstruction/spec.k"),
]
START = re.compile(
    r"^\s*(module|configuration|syntax|context|rule|claim|priority)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "macro",
    "macro-rec",
    "simplification",
    "concrete",
    "owise",
    "priority(",
    "symbol(",
    "no-evaluators",
)


def main() -> int:
    total = Counter()
    print("PER_FILE_COUNTS")
    for path in FILES:
        counts = Counter()
        for line in path.read_text().splitlines():
            match = START.match(line)
            if match:
                counts[match.group(1)] += 1
        total.update(counts)
        shown = " ".join(f"{key}={counts[key]}" for key in sorted(counts))
        print(f"{path}: {shown}")
    print("TOTAL_COUNTS")
    print(" ".join(f"{key}={total[key]}" for key in sorted(total)))
    print("SENSITIVE_ATTRIBUTE_LINES")
    for path in FILES:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if any(attribute in line for attribute in ATTRS):
                print(f"{path}:{line_number}: {' '.join(line.split())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
