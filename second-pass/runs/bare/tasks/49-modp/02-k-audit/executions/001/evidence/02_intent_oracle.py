#!/usr/bin/env python3
"""Compare the candidate with an independent literal 2^n mod p oracle."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def literal_modp(n: int, p: int) -> int:
    # Start with the residue class of 2^0, then multiply n times.
    value = 1 % p
    for _ in range(n):
        value = (2 * value) % p
    return value


candidate_path = Path("/tmp/audit-work/fresh/solution.py")
spec = importlib.util.spec_from_file_location("candidate_intent_oracle", candidate_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load {candidate_path}")
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)

inputs = json.loads(
    Path("/audit-output/evidence/02_inputs.json").read_text(encoding="utf-8")
)["intended_unique"]
mismatches = []
for n, p in inputs:
    expected = literal_modp(n, p)
    actual = candidate.modp(n, p)
    if expected != actual:
        mismatches.append(
            {"input": [n, p], "literal_modp": expected, "candidate": actual}
        )

print("oracle=reviewer-authored repeated modular multiplication with initial 1 % p")
print(f"scope_cases={len(inputs)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
