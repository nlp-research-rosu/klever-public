#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential for problem 84."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


canonical = load_entry(
    Path("/reference/canonical.py"), "trusted_problem_84_canonical"
)
candidate = load_entry(
    Path("/tmp/audit-work/candidate-src/solution.py"), "audited_problem_84_candidate"
)

documented = {1000: "1", 150: "110", 147: "1100"}
boundaries = [
    0,
    1,
    8,
    9,
    10,
    11,
    98,
    99,
    100,
    101,
    998,
    999,
    1000,
    1001,
    9998,
    9999,
    10000,
]
rng = random.Random(840084)
representative_generated = sorted(rng.sample(range(0, 10001), 128))
exhaustive = range(0, 10001)

errors: list[dict[str, object]] = []
for n, expected in documented.items():
    got_reference = canonical(n)
    got_candidate = candidate(n)
    if got_reference != expected or got_candidate != expected:
        errors.append(
            {
                "kind": "documented",
                "n": n,
                "expected": expected,
                "reference": got_reference,
                "candidate": got_candidate,
            }
        )

rows: list[str] = []
for n in exhaustive:
    try:
        got_reference = canonical(n)
    except Exception as exc:  # pragma: no cover - retained as audit evidence
        got_reference = f"EXC:{type(exc).__name__}:{exc}"
    try:
        got_candidate = candidate(n)
    except Exception as exc:  # pragma: no cover - retained as audit evidence
        got_candidate = f"EXC:{type(exc).__name__}:{exc}"
    rows.append(f"{n}:{got_reference}:{got_candidate}\n")
    if (
        got_reference != got_candidate
        or not isinstance(got_reference, str)
        or not isinstance(got_candidate, str)
    ):
        errors.append(
            {
                "kind": "exhaustive",
                "n": n,
                "reference": got_reference,
                "candidate": got_candidate,
            }
        )

digest = hashlib.sha256("".join(rows).encode()).hexdigest()
manifest = {
    "formal_domain": "every integer N with 0 <= N <= 10000",
    "empty_case": "not applicable to an integer input; N=0 is the lower boundary",
    "documented_examples": documented,
    "decimal_place_boundaries": boundaries,
    "representative_generated_seed": 840084,
    "representative_generated": representative_generated,
    "exhaustive_range": {"start": 0, "stop_inclusive": 10000, "count": 10001},
}
print(json.dumps(manifest, sort_keys=True))
print(f"result_rows_sha256={digest}")
print(f"mismatch_count={len(errors)}")
if errors:
    print(json.dumps(errors[:50], sort_keys=True))
    sys.exit(1)
