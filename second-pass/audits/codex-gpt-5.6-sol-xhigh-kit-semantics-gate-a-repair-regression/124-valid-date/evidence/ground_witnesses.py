#!/usr/bin/env python3
"""Ground instances of both entry preconditions and the claimed result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def claimed_ten_result(value: str) -> bool:
    assert len(value) == 10
    codes = list(map(ord, value))
    digits = all(48 <= codes[index] <= 57 for index in (0, 1, 3, 4, 6, 7, 8, 9))
    if not digits or codes[2] != 45 or codes[5] != 45:
        return False
    month = (codes[0] - 48) * 10 + codes[1] - 48
    day = (codes[3] - 48) * 10 + codes[4] - 48
    month_day_ok = (
        1 <= month <= 12
        and day >= 1
        and (
            (month == 2 and day <= 29)
            or (month in (4, 6, 9, 11) and day <= 30)
            or (month not in (2, 4, 6, 9, 11) and day <= 31)
        )
    )
    return month_day_ok


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "witness_canonical")
generated = load(Path("/tmp/audit-work/src/solution.py"), "witness_generated")

witnesses = (
    ("non-ten", "", False),
    ("ten", "03-11-2000", claimed_ten_result("03-11-2000")),
    ("ten", "15-01-2012", claimed_ten_result("15-01-2012")),
    ("ten", "04-30-2000", claimed_ten_result("04-30-2000")),
)

generated_disagreements = 0
canonical_disagreements = 0
for claim, value, claimed_result in witnesses:
    precondition = len(value) != 10 if claim == "non-ten" else len(value) == 10
    generated_result = generated(value)
    canonical_result = canonical(value)
    generated_disagreements += generated_result != claimed_result
    canonical_disagreements += canonical_result != claimed_result
    print(
        json.dumps(
            {
                "claim": claim,
                "input": value,
                "precondition_satisfied": precondition,
                "claimed_result": claimed_result,
                "generated_python": generated_result,
                "canonical_python": canonical_result,
            },
            sort_keys=True,
        )
    )

print(f"generated_claim_disagreements={generated_disagreements}")
print(f"canonical_claim_disagreements={canonical_disagreements}")
raise SystemExit(1 if generated_disagreements else 0)
