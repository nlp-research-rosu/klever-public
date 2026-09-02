#!/usr/bin/env python3
"""Independent differential check of HumanEval/15 candidate against canonical."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load_entry("trusted_canonical_15", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_solution_15",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)

# Examples; the n < 0 branch boundary (-1/0); the loop boundary (0/1);
# nearby values; larger representatives; and a reproducible broader sample.
named_inputs = [-1000, -3, -2, -1, 0, 1, 2, 5, 12, 50, 100, 500]
rng = random.Random(150026)
generated_inputs = [rng.randint(-500, 500) for _ in range(200)]
inputs = list(dict.fromkeys(named_inputs + list(range(-8, 17)) + generated_inputs))

print("COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 "
      "/audit-output/evidence/differential_test.py")
print("oracle=/reference/canonical.py:string_sequence")
print("candidate=/tmp/audit-work/reconstruction/solution.py:string_sequence")
print(f"input_count={len(inputs)}")
print("inputs=" + json.dumps(inputs, separators=(",", ":")))
mismatches = []
for value in inputs:
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append(
            {"n": value, "canonical": expected, "candidate": actual}
        )
for value in (-1, 0, 1, 5, 12):
    print(
        f"witness n={value}: canonical={canonical(value)!r}; "
        f"candidate={candidate(value)!r}"
    )
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print("mismatches=" + json.dumps(mismatches, ensure_ascii=False))
    raise SystemExit(1)
print("SCRIPT_EXIT=0")
