#!/usr/bin/env python3
"""Parse the final MPY scope and compare it with independent Python values."""

from __future__ import annotations

import json
import re
from pathlib import Path


expected = json.loads(
    Path("/tmp/audit-work/160-do-algebra/05_eval_expected.json").read_text()
)
output = Path("/audit-output/evidence/05_eval_bridge_krun.out").read_text()
actual = {
    name: int(value)
    for name, value in re.findall(r'"(case_\d{3})"\s+\|->\s+(-?\d+)', output)
}
mismatches = {
    name: {"expected": expected[name], "actual": actual.get(name)}
    for name in expected
    if actual.get(name) != expected[name]
}
extras = sorted(set(actual) - set(expected))
print(f"expected_cases={len(expected)} parsed_cases={len(actual)}")
print(f"mismatches={len(mismatches)} extras={len(extras)}")
if mismatches:
    print(json.dumps(mismatches, indent=2, sort_keys=True))
if extras:
    print(f"extras={extras}")
if mismatches or extras:
    raise SystemExit(1)
print("RESULT: PASS")
