#!/usr/bin/env python3
"""Compare fresh concrete K results with both independent Python executions."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


canonical = load_entry("trusted_canonical_concrete", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_solution_concrete", Path("/tmp/audit-work/rebuild/solution.py")
)

cases = {
    30: Path("/audit-output/evidence/stage3-krun-a30.log"),
    10: Path("/audit-output/evidence/stage3-krun-a10.log"),
    0: Path("/audit-output/evidence/stage3-krun-a0.log"),
    8: Path("/audit-output/evidence/stage3-krun-a8.log"),
    97: Path("/audit-output/evidence/stage3-krun-a97.log"),
    98: Path("/audit-output/evidence/stage3-krun-a98.log"),
    99: Path("/audit-output/evidence/stage3-krun-a99.log"),
    -7: Path("/audit-output/evidence/stage3-krun-a-minus7.log"),
}

mismatches: list[tuple[int, bool, bool, bool]] = []
for value, log_path in cases.items():
    text = log_path.read_text(encoding="utf-8")
    matches = re.findall(r"Bool\s*\(\s*(true|false)\s*\)", text)
    if len(matches) != 1:
        raise RuntimeError(f"expected one Bool result in {log_path}, got {matches}")
    k_result = matches[0] == "true"
    canonical_result = canonical(value)
    generated_result = generated(value)
    print(
        f"A={value} K={k_result} canonical={canonical_result} "
        f"generated={generated_result}"
    )
    if not (k_result == canonical_result == generated_result):
        mismatches.append((value, k_result, canonical_result, generated_result))

print("mismatch_count=", len(mismatches))
print("mismatches=", mismatches)
if mismatches:
    raise SystemExit(1)
