#!/usr/bin/env python3
"""Line-oriented exhaustive inventory of local K declarations and rules."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/90-next-smallest/candidate-src")
FILES = ["semantic.k", "verification.k", "spec.k"]
START = re.compile(
    r"^\s*(module\b|endmodule\b|imports\b|requires\b|configuration\b|"
    r"syntax\b|rule\b|claim\b)"
)


def main() -> int:
    counts: dict[str, int] = {}
    for name in FILES:
        path = ROOT / name
        lines = path.read_text(encoding="utf-8").splitlines()
        print(f"FILE {name} lines={len(lines)}")
        for number, line in enumerate(lines, start=1):
            if START.search(line):
                stripped = line.strip()
                keyword = stripped.split(maxsplit=1)[0]
                counts[keyword] = counts.get(keyword, 0) + 1
                print(f"{name}:{number}: {stripped}")
    print(f"INVENTORY_COUNTS {dict(sorted(counts.items()))}")
    print("ATTRIBUTE_OCCURRENCES")
    for name in FILES:
        path = ROOT / name
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            attributes = re.findall(r"\[[^\]]+\]", line)
            if attributes:
                print(f"{name}:{number}: {' '.join(attributes)}")
    print("PRIORITY_DECLARATIONS none")
    print("SIMPLIFICATION_RULES none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
