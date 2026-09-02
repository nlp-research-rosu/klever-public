#!/usr/bin/env python3
"""Differentially compare the trusted canonical and submitted Python entry points."""

from __future__ import annotations

import importlib.util
import hashlib
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
submitted = load_entry(
    Path("/tmp/audit-work/33-sort-third/solution.py"), "submitted_solution"
)

cases: list[list[object]] = [
    [],
    [1],
    [2, 1],
    [1, 2, 3],
    [3, 2, 1, 0],
    [5, 6, 3, 4, 8, 9, 2],
    [9, -1, 8, 6, -2, 5, 3, -3, 2, 0],
    [4, 4, 4, 4, 4, 4, 4],
    ["z", "keep1", "keep2", "a", "keep4", "keep5", "m"],
    [3.5, -1.0, 7.25, 2.0, 0.0, 8.0, -4.5],
]

# Exhaust the modulo-3 branch boundaries at small lengths.
for length in range(0, 8):
    for values in itertools.product((-2, 0, 2), repeat=length):
        cases.append(list(values))

rng = random.Random(0x33)
for _ in range(5000):
    length = rng.randrange(0, 81)
    cases.append([rng.randrange(-1000, 1001) for _ in range(length)])

case_path = Path("/audit-output/evidence/differential_inputs.jsonl")
with case_path.open("w", encoding="utf-8") as stream:
    for index, original in enumerate(cases):
        stream.write(json.dumps({"case": index, "input": original}) + "\n")

for index, original in enumerate(cases):
    canonical_input = list(original)
    submitted_input = list(original)
    expected = canonical(canonical_input)
    actual = submitted(submitted_input)
    if actual != expected:
        raise AssertionError(
            f"mismatch case={index} input={original!r} "
            f"canonical={expected!r} submitted={actual!r}"
        )
    if canonical_input != original or submitted_input != original:
        raise AssertionError(f"unexpected input mutation at case={index}")

case_hash = hashlib.sha256(case_path.read_bytes()).hexdigest()
print(
    f"cases={len(cases)} mismatches=0 input_mutations=0 "
    f"input_sha256={case_hash}"
)
