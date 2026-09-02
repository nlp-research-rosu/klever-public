#!/usr/bin/env python3
"""Generate deterministic concrete K assertions from the trusted Python oracle."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parser = argparse.ArgumentParser()
parser.add_argument("--solution", type=Path, required=True)
parser.add_argument("--canonical", type=Path, required=True)
parser.add_argument("--python-out", type=Path, required=True)
parser.add_argument("--cases-out", type=Path, required=True)
args = parser.parse_args()

canonical = load(args.canonical, "trusted_canonical_for_k")
candidate = load(args.solution, "candidate_for_k")

cases = [
    [15, 33, 1422, 1],
    [152, 323, 1422, 10],
    [],
    [1],
    [2],
    [9, 10, 11, 12, 19, 20],
    [99, 15, 15, 1],
    [101, 111, 13579, 20],
]
rng = random.Random(104_700)
for _ in range(56):
    cases.append(
        [rng.randrange(1, 100_000) for _ in range(rng.randrange(0, 7))]
    )

records = []
assertions = []
for values in cases:
    expected = canonical.unique_digits(list(values))
    actual = candidate.unique_digits(list(values))
    if actual != expected:
        raise AssertionError((values, expected, actual))
    records.append({"input": values, "expected": expected})
    assertions.append(f"assert unique_digits({values!r}) == {expected!r}")

source = args.solution.read_text()
args.python_out.write_text(source + "\n\n" + "\n".join(assertions) + "\n")
args.cases_out.write_text(json.dumps(records, separators=(",", ":")) + "\n")
print(f"k_concrete_case_count={len(cases)}")
print(f"python_candidate_mismatch_count=0")
