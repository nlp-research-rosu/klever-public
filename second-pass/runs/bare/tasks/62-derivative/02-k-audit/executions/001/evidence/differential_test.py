#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 62."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
generated = load_module("generated_solution", Path("/tmp/audit-work/audit-62/solution.py"))

documented_and_boundaries = [
    [3, 1, 2, 4, 5],
    [1, 2, 3],
    [],
    [7],
    [0],
    [0, 0],
    [5, -3],
    [-2, 4, -6],
    [10**30, -(10**30), 1],
    [1.5, -2.0, 0.25],
    [True, False, True],
    list(range(998)),
    list(range(1100)),
]

rng = random.Random(620062)
generated_integer_inputs = [
    [rng.randint(-10**6, 10**6) for _ in range(length)]
    for length in range(0, 17)
    for _ in range(40)
]
generated_float_inputs = [
    [rng.randint(-4000, 4000) / 8.0 for _ in range(length)]
    for length in range(0, 9)
    for _ in range(12)
]
generated_inputs = generated_integer_inputs + generated_float_inputs
inputs = documented_and_boundaries + generated_inputs

mismatches = []
results = []
def observe(function, xs):
    try:
        return {"kind": "return", "value": function(list(xs))}
    except Exception as error:  # The exception is an observable differential result.
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}


def concise(outcome):
    if outcome["kind"] == "exception":
        return {"kind": "exception", "type": outcome["type"]}
    value = outcome["value"]
    rendered = repr(value).encode("utf-8")
    return {
        "kind": "return",
        "value_length": len(value) if isinstance(value, list) else None,
        "repr_sha256": hashlib.sha256(rendered).hexdigest(),
    }


for index, xs in enumerate(inputs):
    expected = observe(canonical.derivative, xs)
    actual = observe(generated.derivative, xs)
    record = {"input": xs, "canonical": expected, "generated": actual}
    results.append(record)
    if actual != expected:
        mismatches.append(
            {
                "case_index": index,
                "input_length": len(xs),
                "input_head": xs[:5],
                "input_tail": xs[-5:],
                "canonical": concise(expected),
                "generated": concise(actual),
            }
        )

summary = {
    "oracle": "/reference/canonical.py:derivative",
    "subject": "/tmp/audit-work/audit-62/solution.py:derivative",
    "seed": 620062,
    "documented_and_boundary_cases": len(documented_and_boundaries),
    "generated_integer_cases": len(generated_integer_inputs),
    "generated_float_cases": len(generated_float_inputs),
    "generated_cases": len(generated_inputs),
    "total_cases": len(inputs),
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
}

Path("/audit-output/evidence/differential_inputs_results.json").write_text(
    json.dumps({"summary": summary, "cases": results}, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(summary, indent=2))
raise SystemExit(1 if mismatches else 0)
