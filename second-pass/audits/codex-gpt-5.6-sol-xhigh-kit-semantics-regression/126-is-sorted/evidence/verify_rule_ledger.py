#!/usr/bin/env python3
"""Check that the grouped static-review ledger covers each inventory entry."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


inventory = Path("/audit-output/evidence/k_rule_inventory.txt").read_text()
ledger = Path("/audit-output/evidence/rule_review_ledger.md").read_text()

expected = {
    int(number)
    for number in re.findall(r"^ENTRY\s+(\d+)\s", inventory, re.MULTILINE)
}
covered: list[int] = []
for lo_text, hi_text in re.findall(r"^\|\s*(\d{4})(?:–(\d{4}))?\s*\|", ledger, re.MULTILINE):
    lo = int(lo_text)
    hi = int(hi_text or lo_text)
    covered.extend(range(lo, hi + 1))

counts = Counter(covered)
actual = set(covered)
missing = sorted(expected - actual)
extra = sorted(actual - expected)
duplicates = sorted(number for number, count in counts.items() if count != 1)

print(f"inventory_entries={len(expected)}")
print(f"ledger_unique_entries={len(actual)}")
print(f"missing={missing}")
print(f"extra={extra}")
print(f"duplicate_or_multiply_covered={duplicates}")
raise SystemExit(int(bool(missing or extra or duplicates)))
