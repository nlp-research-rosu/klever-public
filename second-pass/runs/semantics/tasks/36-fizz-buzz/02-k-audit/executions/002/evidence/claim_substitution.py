#!/usr/bin/env python3
"""Extract each fixed entry theorem and compare it to both Python executions."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reviewer-002/scratch")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


canonical = load_entry("pinning_canonical", SCRATCH / "canonical.py")
generated = load_entry("pinning_solution", SCRATCH / "solution.py")
spec_text = (SCRATCH / "spec.k").read_text(encoding="utf-8")
entries = [
    (int(n_text), int(result_text))
    for n_text, result_text in re.findall(
        r"Call\(FIZZ-BUZZ-CLOSURE,\s*(-?\d+)\)\s*=>\s*(-?\d+)",
        spec_text,
    )
]
print(f"entry_claims={entries}")
print(f"entry_claim_count={len(entries)}")
mismatches = []
for n, claimed in entries:
    canonical_result = canonical(n)
    generated_result = generated(n)
    print(
        f"n={n} claimed={claimed} canonical={canonical_result} "
        f"generated={generated_result}"
    )
    if not (claimed == canonical_result == generated_result):
        mismatches.append((n, claimed, canonical_result, generated_result))
print(f"mismatch_count={len(mismatches)}")
raise SystemExit(bool(mismatches))
