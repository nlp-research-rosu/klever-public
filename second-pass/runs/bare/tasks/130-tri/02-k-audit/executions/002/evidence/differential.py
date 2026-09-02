#!/usr/bin/env python3
"""Independent candidate/canonical/contract differential for HumanEval 130."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/130-tri-audit")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_oracle(n: int) -> list[int]:
    assert n >= 0
    values = [1]
    for i in range(1, n + 1):
        if i == 1:
            values.append(3)
        elif i % 2 == 0:
            values.append(1 + i // 2)
        else:
            values.append(values[i - 1] + values[i - 2] + (1 + (i + 1) // 2))
    return values


def outcome(function, n: int):
    try:
        value = function(n)
        digest = hashlib.sha256(repr(value).encode()).hexdigest()
        return {
            "status": "return",
            "length": len(value),
            "last": value[-1],
            "repr_sha256": digest,
            "value": value if n <= 10 else None,
        }
    except Exception as error:  # The exception class is part of the observation.
        return {
            "status": "raise",
            "exception": type(error).__name__,
            "message": str(error),
        }


canonical = load_module("trusted_canonical_130", SCRATCH / "canonical.py")
candidate = load_module("generated_candidate_130", SCRATCH / "solution.py")

documented = [3]
boundaries = list(range(0, 11))
representative_range = list(range(0, 301))
random.seed(130)
generated = sorted(set(random.randrange(0, 901) for _ in range(128)))
large_recursion_probes = [950, 975, 990, 995, 996, 997, 998, 999, 1000, 1001, 1100]
ordinary = sorted(set(documented + boundaries + representative_range + generated))

ordinary_mismatches = []
type_differences = []
for n in ordinary:
    trusted = canonical.tri(n)
    generated_value = candidate.tri(n)
    expected = contract_oracle(n)
    if generated_value != trusted or generated_value != expected:
        ordinary_mismatches.append(
            {
                "n": n,
                "canonical": outcome(canonical.tri, n),
                "candidate": outcome(candidate.tri, n),
                "oracle": outcome(contract_oracle, n),
            }
        )
    if [type(value).__name__ for value in generated_value] != [
        type(value).__name__ for value in trusted
    ]:
        type_differences.append(n)

large_results = []
large_status_mismatches = []
for n in large_recursion_probes:
    trusted_outcome = outcome(canonical.tri, n)
    candidate_outcome = outcome(candidate.tri, n)
    oracle_outcome = outcome(contract_oracle, n)
    record = {
        "n": n,
        "canonical": trusted_outcome,
        "candidate": candidate_outcome,
        "oracle": oracle_outcome,
    }
    large_results.append(record)
    if (
        candidate_outcome["status"] != trusted_outcome["status"]
        or candidate_outcome["status"] != oracle_outcome["status"]
    ):
        large_status_mismatches.append(record)

print(f"PYTHON_VERSION={sys.version.split()[0]}")
print(f"PYTHON_RECURSION_LIMIT={sys.getrecursionlimit()}")
print(f"DOCUMENTED_INPUTS={documented}")
print(f"BOUNDARY_INPUTS={boundaries}")
print("REPRESENTATIVE_RANGE=0..300 inclusive")
print(f"SEEDED_GENERATED_INPUTS={generated}")
print(f"LARGE_RECURSION_PROBES={large_recursion_probes}")
print(f"ORDINARY_CASE_COUNT={len(ordinary)}")
print(f"ORDINARY_VALUE_MISMATCH_COUNT={len(ordinary_mismatches)}")
print(f"CANONICAL_CANDIDATE_ELEMENT_TYPE_DIFFERENCE_COUNT={len(type_differences)}")
print(f"TYPE_DIFFERENCE_FIRST_INPUTS={type_differences[:12]}")
print(f"LARGE_STATUS_MISMATCH_COUNT={len(large_status_mismatches)}")
print("LARGE_RESULTS=")
print(json.dumps(large_results, indent=2, sort_keys=True))
print("ORDINARY_MISMATCHES=")
print(json.dumps(ordinary_mismatches, indent=2, sort_keys=True))

if ordinary_mismatches:
    raise SystemExit(1)
if not large_status_mismatches:
    raise SystemExit("expected recursion-limit divergence was not observed")
