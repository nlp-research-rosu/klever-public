#!/usr/bin/env python3
"""Independent candidate-versus-trusted-canonical differential test."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/36-fizz-buzz-audit-002")
CANONICAL_PATH = SCRATCH / "trusted" / "canonical.py"
CANDIDATE_PATH = SCRATCH / "candidate" / "solution.py"
INPUTS_PATH = Path("/audit-output/evidence/stage2/differential_inputs.json")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


canonical = load_function("trusted_canonical", CANONICAL_PATH)
candidate = load_function("candidate_solution", CANDIDATE_PATH)

documented = [50, 78, 79]
empty_and_boundary = [
    -50,
    -1,
    0,
    1,
    10,
    11,
    12,
    13,
    14,
    22,
    26,
    65,
    66,
    67,
    76,
    77,
    78,
    79,
    80,
    116,
    117,
    118,
    142,
    143,
    144,
    168,
    169,
    170,
    176,
    177,
    178,
    770,
    771,
    772,
    776,
    777,
    778,
]
exhaustive_small = list(range(-25, 2001))

rng = random.Random(360013)
generated = [rng.randint(-100, 20000) for _ in range(200)]
generated.extend(
    value + delta
    for value in [77, 117, 143, 176, 377, 572, 671, 770, 777, 1177, 1771]
    for delta in [-1, 0, 1, 2]
)

all_inputs = sorted(
    set(documented + empty_and_boundary + exhaustive_small + generated)
)
INPUTS_PATH.write_text(json.dumps(all_inputs, separators=(",", ":")) + "\n")

mismatches = []
for value in all_inputs:
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append({"n": value, "canonical": expected, "candidate": actual})

payload = INPUTS_PATH.read_bytes()
print(f"oracle={CANONICAL_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print(f"documented={documented}")
print(f"input_count={len(all_inputs)}")
print(f"input_min={min(all_inputs)} input_max={max(all_inputs)}")
print(f"inputs_sha256={hashlib.sha256(payload).hexdigest()}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], sort_keys=True))
    raise SystemExit(1)

for value in documented:
    print(f"example n={value} result={candidate(value)}")
