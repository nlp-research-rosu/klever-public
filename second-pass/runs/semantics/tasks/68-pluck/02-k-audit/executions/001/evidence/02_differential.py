#!/usr/bin/env python3
"""Independent differential test for HumanEval 68 pluck.

The complete generated input scope is deterministic:
  * all arrays of lengths 0..6 over values 0..5;
  * 2,500 arrays from Random(680024), lengths 0..100, values 0..1,000,000;
  * the named boundary and documented cases below.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_function(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(
    Path("/tmp/audit-work/68-pluck/solution.py"), "generated_solution"
)

named_cases = [
    ("example-1", [4, 2, 3]),
    ("example-2", [1, 2, 3]),
    ("example-3-empty", []),
    ("example-4-zero-tie", [5, 0, 3, 0, 4, 2]),
    ("single-odd", [1]),
    ("single-zero", [0]),
    ("single-positive-even", [2]),
    ("all-odd", [1, 3, 5, 7]),
    ("first-even-remains-min", [2, 7, 4]),
    ("later-even-strictly-smaller", [8, 7, 4]),
    ("equal-minimum-keeps-first-index", [6, 2, 9, 2]),
    ("odd-before-first-even", [9, 4]),
    ("zero-at-end", [9, 7, 0]),
    ("large-unbounded-value", [10**100 + 1, 10**100, 2]),
    ("max-length-even-first", [0] + [1] * 9999),
    ("max-length-even-last", [1] * 9999 + [2]),
    ("max-length-equal-tie", [4] + [1] * 9998 + [4]),
]

rng = random.Random(680024)
random_cases = [
    [rng.randint(0, 1_000_000) for _ in range(rng.randint(0, 100))]
    for _ in range(2500)
]

cases = [(name, values) for name, values in named_cases]
for length in range(7):
    for values in itertools.product(range(6), repeat=length):
        cases.append((f"exhaustive-len-{length}", list(values)))
cases.extend(("random-seed-680024", values) for values in random_cases)

digest = hashlib.sha256()
mismatches = []
mutations = []
for ordinal, (label, values) in enumerate(cases):
    before = list(values)
    expected = canonical(values)
    actual = generated(values)
    digest.update(
        json.dumps([label, values], separators=(",", ":")).encode("utf-8")
    )
    digest.update(b"\n")
    if values != before:
        mutations.append(
            {"ordinal": ordinal, "label": label, "before": before, "after": values}
        )
    if actual != expected:
        mismatches.append(
            {
                "ordinal": ordinal,
                "label": label,
                "input": values,
                "canonical": expected,
                "generated": actual,
            }
        )

named_manifest = []
for label, values in named_cases:
    encoded = json.dumps(values, separators=(",", ":")).encode("utf-8")
    named_manifest.append(
        {
            "label": label,
            "length": len(values),
            "values": values if len(values) <= 20 else None,
            "sha256": hashlib.sha256(encoded).hexdigest(),
        }
    )
print("named_case_manifest=" + json.dumps(named_manifest, separators=(",", ":")))
print("exhaustive_scope=lengths 0..6 over values 0..5")
print("random_scope=2500 arrays; seed=680024; lengths 0..100; values 0..1000000")
print("total_cases=" + str(len(cases)))
print("input_manifest_sha256=" + digest.hexdigest())
print("input_mutations=" + str(len(mutations)))
print("mismatches=" + str(len(mismatches)))
if mutations:
    print("first_input_mutation=" + json.dumps(mutations[0], separators=(",", ":")))
if mismatches:
    print("first_mismatch=" + json.dumps(mismatches[0], separators=(",", ":")))
    sys.exit(1)
