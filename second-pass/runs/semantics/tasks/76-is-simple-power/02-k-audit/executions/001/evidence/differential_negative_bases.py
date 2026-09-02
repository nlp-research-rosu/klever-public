#!/usr/bin/env python3
"""Probe the prompt's unstated negative-base boundary.

For n <= -2 the trusted canonical loop terminates for every integer x: the
absolute value grows and every second product is positive.  This makes the
range safe for direct differential testing without timeout assumptions.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/76-is-simple-power")


def load_function(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


canonical = load_function("trusted_canonical_negative", SCRATCH / "trusted/canonical.py")
generated = load_function(
    "generated_solution_negative", SCRATCH / "candidate-source/solution.py"
)

cases = [(x, n) for x in range(-25, 1001) for n in range(-20, -1)]
mismatches = []
for x, n in cases:
    expected = canonical(x, n)
    actual = generated(x, n)
    if actual != expected:
        mismatches.append((x, n, expected, actual))

print("scope=all x in [-25,1000], all n in [-20,-2]")
print(f"case_count={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
print(f"first_mismatches={mismatches[:20]}")
if not mismatches:
    raise SystemExit("expected this probe to expose the negative-base discrepancy")
