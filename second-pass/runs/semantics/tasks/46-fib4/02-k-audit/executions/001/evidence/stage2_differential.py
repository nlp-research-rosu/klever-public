#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval problem 46."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


canonical = load_function(
    Path("/tmp/audit-work/46-fib4-audit/reference/canonical.py"),
    "trusted_canonical",
)
candidate = load_function(
    Path("/tmp/audit-work/46-fib4-audit/candidate-src/solution.py"),
    "generated_solution",
)

# Explicit contract examples, all base/branch boundaries, the first twenty
# recurrence points, and a deterministic broader generated sample.
documented_examples = [5, 6, 7]
boundary_cases = [0, 1, 2, 3, 4]
small_recurrence_cases = list(range(5, 25))
rng = random.Random(4604)
generated_cases = [rng.randrange(0, 501) for _ in range(128)]
inputs = list(
    dict.fromkeys(
        documented_examples
        + boundary_cases
        + small_recurrence_cases
        + generated_cases
        + [50, 100, 128, 200, 257, 500]
    )
)

mismatches: list[dict[str, object]] = []
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected:
        mismatches.append({"n": n, "canonical": expected, "candidate": actual})

# Negative indexes are outside the sequence's intended n >= 0 domain, but
# record them so the audit does not silently imply whole-Python-int equality.
excluded_negative_probes: list[dict[str, object]] = []
for n in [-5, -4, -3, -2, -1]:
    row: dict[str, object] = {"n": n}
    for label, func in (("canonical", canonical), ("candidate", candidate)):
        try:
            row[label] = {"returned": func(n)}
        except Exception as exc:  # evidence records exception class, not message
            row[label] = {"raised": type(exc).__name__}
    excluded_negative_probes.append(row)

result = {
    "oracle": "/tmp/audit-work/46-fib4-audit/reference/canonical.py:fib4",
    "implementation": "/tmp/audit-work/46-fib4-audit/candidate-src/solution.py:fib4",
    "intended_domain": "integers n >= 0",
    "documented_examples": documented_examples,
    "boundary_cases": boundary_cases,
    "inputs": inputs,
    "case_count": len(inputs),
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
    "excluded_negative_probes": excluded_negative_probes,
}
print(json.dumps(result, indent=2, sort_keys=True))
sys.exit(1 if mismatches else 0)
