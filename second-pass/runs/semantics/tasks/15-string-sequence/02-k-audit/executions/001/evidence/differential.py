#!/usr/bin/env python3
"""Independent differential check of trusted canonical.py versus solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load_function(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
)
candidate = load_function(
    Path("/tmp/audit-work/reconstruction/solution.py"), "generated_solution"
)

# Examples; negative empty-range behavior; each source branch boundary; decimal
# width boundaries; and deterministic representative generated integers.
fixed = [
    -100,
    -20,
    -2,
    -1,
    0,
    1,
    2,
    5,
    8,
    9,
    10,
    11,
    98,
    99,
    100,
    101,
    999,
    1000,
]
rng = random.Random(150015)
generated = [rng.randint(-100, 300) for _ in range(128)]
inputs = list(dict.fromkeys(fixed + generated))

records = []
mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    record = {
        "n": n,
        "canonical": expected,
        "candidate": actual,
        "canonical_sha256": hashlib.sha256(expected.encode()).hexdigest(),
        "candidate_sha256": hashlib.sha256(actual.encode()).hexdigest(),
        "equal": expected == actual,
    }
    records.append(record)
    if expected != actual:
        mismatches.append(record)

print(
    json.dumps(
        {
            "oracle": "/tmp/audit-work/trusted/canonical.py:string_sequence",
            "candidate": "/tmp/audit-work/reconstruction/solution.py:string_sequence",
            "fixed_inputs": fixed,
            "generated_seed": 150015,
            "generated_count_before_deduplication": len(generated),
            "complete_inputs": inputs,
            "case_count": len(inputs),
            "mismatch_count": len(mismatches),
            "records": records,
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches else 0)
