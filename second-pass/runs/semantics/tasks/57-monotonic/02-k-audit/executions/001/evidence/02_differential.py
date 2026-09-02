#!/usr/bin/env python3
"""Independent differential test for HumanEval 57 monotonic."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path

EVIDENCE = Path("/audit-output/evidence")
WORK = Path("/tmp/audit-work/57-monotonic")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.monotonic


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(WORK / "solution.py", "generated_solution")

named_cases = [
    ("documented-ascending", [1, 2, 4, 20]),
    ("documented-zigzag", [1, 20, 4, 10]),
    ("documented-descending", [4, 1, 0, -10]),
    ("empty", []),
    ("singleton", [3]),
    ("equal-pair", [1, 1]),
    ("strict-increase-pair", [1, 2]),
    ("strict-decrease-pair", [2, 1]),
    ("nondecreasing-with-equality", [1, 1, 2, 2]),
    ("nonincreasing-with-equality", [2, 2, 1, 1]),
    ("all-equal", [0, 0, 0, 0]),
    ("rise-then-fall", [0, 1, 0]),
    ("fall-then-rise", [1, 0, 1]),
    ("late-decrease", [-2, -1, 0, -1]),
    ("late-increase", [2, 1, 0, 1]),
    ("large-boundaries", [-(2**63), 0, 2**63 - 1]),
    ("homogeneous-strings-up", ["a", "a", "b"]),
    ("homogeneous-strings-down", ["z", "b", "b"]),
    ("homogeneous-strings-zigzag", ["a", "z", "b"]),
]

exhaustive_cases = [
    list(values)
    for length in range(0, 6)
    for values in itertools.product(range(-2, 3), repeat=length)
]

rng = random.Random(570057)
random_cases = [
    [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 15))]
    for _ in range(1000)
]

records = []
mismatches = []
exceptions = []
for category, labeled_cases in [
    ("named", [(name, values) for name, values in named_cases]),
    ("exhaustive", [(str(i), values) for i, values in enumerate(exhaustive_cases)]),
    ("random", [(str(i), values) for i, values in enumerate(random_cases)]),
]:
    for label, values in labeled_cases:
        record = {"category": category, "label": label, "input": values}
        try:
            expected = canonical(values.copy())
            actual = generated(values.copy())
            record.update(expected=expected, actual=actual)
            if expected != actual:
                mismatches.append(record)
        except Exception as error:  # retained as visible evidence
            record["exception"] = f"{type(error).__name__}: {error}"
            exceptions.append(record)
        records.append(record)

inputs_path = EVIDENCE / "02_differential_inputs.json"
inputs_path.write_text(
    json.dumps(
        {
            "named": [{"label": name, "input": values} for name, values in named_cases],
            "exhaustive_domain": {
                "element_values": [-2, -1, 0, 1, 2],
                "lengths": [0, 1, 2, 3, 4, 5],
                "inputs": exhaustive_cases,
            },
            "random": {
                "seed": 570057,
                "count": len(random_cases),
                "value_range": [-1000, 1000],
                "length_range": [0, 15],
                "inputs": random_cases,
            },
        },
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

encoded_inputs = inputs_path.read_bytes()
print(f"named_cases={len(named_cases)}")
print(f"exhaustive_cases={len(exhaustive_cases)}")
print(f"random_cases={len(random_cases)}")
print(f"total_cases={len(records)}")
print(f"exceptions={len(exceptions)}")
print(f"mismatches={len(mismatches)}")
print(f"inputs_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")
for record in records[: len(named_cases)]:
    print(
        "named_result="
        + json.dumps(record, sort_keys=True, separators=(",", ":"))
    )
if exceptions:
    print("exception_records=" + json.dumps(exceptions, sort_keys=True))
if mismatches:
    print("mismatch_records=" + json.dumps(mismatches, sort_keys=True))
raise SystemExit(1 if exceptions or mismatches else 0)
