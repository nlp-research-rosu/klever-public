#!/usr/bin/env python3
"""Final consistency checks for the review and reviewer evidence."""

from __future__ import annotations

import ast
import json
import stat
from pathlib import Path


OUTPUT = Path("/audit-output")
EVIDENCE = OUTPUT / "evidence"
REVIEW = OUTPUT / "REVIEW.md"


def main() -> int:
    review = REVIEW.read_text()
    lines = review.splitlines()
    expected_tail = ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
    print(f"review bytes: {REVIEW.stat().st_size}")
    print(f"review final two lines: {lines[-2:]}")
    print(f"exact required tail: {lines[-2:] == expected_tail}")
    print(f"VERDICT marker count: {sum(line.startswith('VERDICT:') for line in lines)}")
    print(
        "LEGITIMACY marker count: "
        f"{sum(line.startswith('LEGITIMACY:') for line in lines)}"
    )

    inventory = json.loads((EVIDENCE / "stage5-rule-inventory.json").read_text())
    print(f"inventory entry count: {inventory['entry_count']}")
    print(f"inventory actual entries: {len(inventory['entries'])}")
    print(f"inventory rule count: {inventory['kind_counts']['rule']}")

    python_files = sorted(EVIDENCE.glob("*.py"))
    for path in python_files:
        ast.parse(path.read_text(), filename=str(path))
    print(f"reviewer Python scripts parsed: {len(python_files)}")

    irregular = []
    for path in EVIDENCE.iterdir():
        mode = path.lstat().st_mode
        if not stat.S_ISREG(mode):
            irregular.append(path.name)
    print(f"non-regular evidence entries: {irregular}")

    checks = [
        lines[-2:] == expected_tail,
        sum(line.startswith("VERDICT:") for line in lines) == 1,
        sum(line.startswith("LEGITIMACY:") for line in lines) == 1,
        inventory["entry_count"] == len(inventory["entries"]) == 1115,
        inventory["kind_counts"]["rule"] == 704,
        not irregular,
    ]
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
