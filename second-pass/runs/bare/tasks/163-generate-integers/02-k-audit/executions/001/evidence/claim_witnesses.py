#!/usr/bin/env python3
"""Ground witnesses for the formal entry claim and its result expression."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


canonical = load_entry(Path("/reference/canonical.py"), "canonical_claim_witness")
candidate = load_entry(
    Path("/tmp/audit-work/src/solution.py"), "candidate_claim_witness"
)


def formal_expected(a: int, b: int) -> list[int]:
    # Literal ground interpretation of verification.k's four expectedDigit calls.
    return [d for d in (2, 4, 6, 8) if (a <= d <= b) or (b <= d <= a)]


witnesses = [(2, 8), (10, 14), (3, 7)]
records = []
for a, b in witnesses:
    record = {
        "a": a,
        "b": b,
        "precondition_A_gt_0_and_B_gt_0": a > 0 and b > 0,
        "formal_expected": formal_expected(a, b),
        "trusted_canonical": canonical(a, b),
        "candidate_python": candidate(a, b),
    }
    records.append(record)

ok = all(
    record["precondition_A_gt_0_and_B_gt_0"]
    and record["formal_expected"]
    == record["trusted_canonical"]
    == record["candidate_python"]
    for record in records
)
print(json.dumps({"witnesses": records, "all_agree": ok}, sort_keys=True))
raise SystemExit(0 if ok else 1)
