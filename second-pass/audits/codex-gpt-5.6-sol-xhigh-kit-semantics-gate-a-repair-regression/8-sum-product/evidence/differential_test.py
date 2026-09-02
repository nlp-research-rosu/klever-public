#!/usr/bin/env python3
"""Independent differential test for HumanEval 8 sum_product.

Oracle: /reference/canonical.py, loaded directly from the trusted mount.
Candidate: the fresh scratch copy of /candidate/solution.py.
Domain: finite Python lists whose elements are Python integers.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path, module_name: str) -> Callable[[list[int]], tuple[int, int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(
    Path("/tmp/audit-work/reconstruction/solution.py"), "audited_candidate"
)

documented_and_boundaries = [
    [],
    [1, 2, 3, 4],
    [0],
    [1],
    [-1],
    [2],
    [0, 0],
    [-1, 1],
    [1, -1],
    [2, 3],
    [-2, -3],
    [5, 0, -7],
    [-(2**63), 2**63 - 1],
    [10**100],
    [10**100, -(10**100), 0, 7],
]

# Exhaust all lengths 0..4 over a branch-sensitive alphabet, then add
# deterministic broader samples (including longer lists).
alphabet = (-3, -1, 0, 1, 2)
exhaustive_small = [
    list(values)
    for length in range(5)
    for values in itertools.product(alphabet, repeat=length)
]
rng = random.Random(0x8A5)
generated = [
    [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 20))]
    for _ in range(1000)
]

inputs: list[list[int]] = []
seen: set[tuple[int, ...]] = set()
for values in documented_and_boundaries + exhaustive_small + generated:
    key = tuple(values)
    if key not in seen:
        seen.add(key)
        inputs.append(values)

mismatches: list[dict[str, Any]] = []
for values in inputs:
    expected = canonical(list(values))
    actual = candidate(list(values))
    if actual != expected or type(actual) is not type(expected):
        mismatches.append(
            {"input": values, "canonical": repr(expected), "candidate": repr(actual)}
        )

serialized = json.dumps(inputs, separators=(",", ":"), ensure_ascii=True).encode()
scratch_inputs = Path(
    "/tmp/audit-work/reconstruction/differential_inputs.json"
)
scratch_inputs.write_bytes(serialized + b"\n")
summary = {
    "domain": "finite lists of Python integers",
    "documented_cases": documented_and_boundaries[:2],
    "handcrafted_boundary_count": len(documented_and_boundaries),
    "exhaustive_small_generation": {
        "alphabet": list(alphabet),
        "lengths": [0, 1, 2, 3, 4],
    },
    "deterministic_random_seed": "0x8A5",
    "deterministic_random_requested": 1000,
    "unique_input_count": len(inputs),
    "input_json_sha256": hashlib.sha256(serialized).hexdigest(),
    "scratch_input_artifact": str(scratch_inputs),
    "mismatch_count": len(mismatches),
    "first_mismatches": mismatches[:10],
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
