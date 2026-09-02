#!/usr/bin/env python3
"""Independent source-level differential test for HumanEval 163."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_163")
candidate = load_entry(
    Path("/tmp/audit-work/src/solution.py"), "scratch_candidate_solution_163"
)

documented = [(2, 8), (8, 2), (10, 14)]
explicit_boundaries = [
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (2, 3),
    (3, 2),
    (3, 3),
    (3, 4),
    (4, 3),
    (4, 4),
    (4, 5),
    (5, 4),
    (5, 5),
    (5, 6),
    (6, 5),
    (6, 6),
    (6, 7),
    (7, 6),
    (7, 7),
    (7, 8),
    (8, 7),
    (8, 8),
    (8, 9),
    (9, 8),
    (9, 9),
    (9, 10),
    (10, 9),
    (10, 14),
    (14, 10),
]
exhaustive_branch_grid = [(a, b) for a in range(1, 13) for b in range(1, 13)]
large_boundaries = [
    (1, 10**100),
    (10**100, 1),
    (10**100, 10**100),
    (10**100 - 1, 10**100),
]
rng = random.Random(163)
generated = [(rng.randint(1, 10**6), rng.randint(1, 10**6)) for _ in range(500)]

cases = []
seen = set()
for pair in documented + explicit_boundaries + exhaustive_branch_grid + large_boundaries + generated:
    if pair not in seen:
        seen.add(pair)
        cases.append(pair)

mismatches = []
for a, b in cases:
    want = canonical(a, b)
    got = candidate(a, b)
    if type(got) is not list or got != want:
        mismatches.append({"a": a, "b": b, "canonical": want, "candidate": got})

print(
    json.dumps(
        {
            "oracle": "/reference/canonical.py:generate_integers",
            "candidate": "/tmp/audit-work/src/solution.py:generate_integers",
            "documented": documented,
            "explicit_boundaries": explicit_boundaries,
            "exhaustive_grid": {"a": [1, 12], "b": [1, 12]},
            "generated": {"seed": 163, "count": 500, "range": [1, 10**6]},
            "large_boundaries": [[str(a), str(b)] for a, b in large_boundaries],
            "unique_case_count": len(cases),
            "mismatch_count": len(mismatches),
            "mismatches": mismatches[:20],
        },
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches else 0)
