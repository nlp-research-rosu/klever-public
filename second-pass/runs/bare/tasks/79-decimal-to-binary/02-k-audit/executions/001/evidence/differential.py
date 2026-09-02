#!/usr/bin/env python3
"""Independent differential test for the trusted canonical and candidate entry points."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from types import ModuleType
from typing import Any


WORK = Path("/tmp/audit-work")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Any, value: int) -> dict[str, Any]:
    try:
        result = function(value)
        return {"kind": "return", "type": type(result).__name__, "value": result}
    except Exception as error:  # pragma: no cover - retained to compare behavior
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "value": str(error),
        }


def main() -> int:
    canonical = load_module("trusted_canonical", WORK / "canonical.py")
    generated = load_module("candidate_solution", WORK / "solution.py")

    documented_and_boundaries = [
        -1025,
        -1024,
        -1023,
        -33,
        -32,
        -31,
        -17,
        -16,
        -15,
        -5,
        -4,
        -3,
        -2,
        -1,
        0,
        1,
        2,
        3,
        4,
        5,
        7,
        8,
        9,
        15,
        16,
        17,
        31,
        32,
        33,
        63,
        64,
        65,
        1023,
        1024,
        1025,
        2**63 - 1,
        2**63,
        2**63 + 1,
        -(2**63) - 1,
        -(2**63),
        -(2**63) + 1,
        2**4096 + 3,
        -(2**4096 + 3),
    ]
    exhaustive_small = list(range(-2048, 2049))
    rng = random.Random(790079)
    generated_inputs = [
        rng.getrandbits(rng.randrange(1, 1025))
        * (-1 if rng.randrange(2) else 1)
        for _ in range(1000)
    ]
    inputs = list(dict.fromkeys(documented_and_boundaries + exhaustive_small + generated_inputs))

    mismatches: list[dict[str, Any]] = []
    edge_results: list[dict[str, Any]] = []
    edge_set = set(documented_and_boundaries)
    for value in inputs:
        expected = outcome(canonical.decimal_to_binary, value)
        actual = outcome(generated.decimal_to_binary, value)
        record = {"input": str(value), "canonical": expected, "candidate": actual}
        if value in edge_set:
            edge_results.append(record)
        if expected != actual:
            mismatches.append(record)

    report = {
        "oracle": "/tmp/audit-work/canonical.py copied from /reference/canonical.py",
        "candidate": "/tmp/audit-work/solution.py copied from /candidate/solution.py",
        "domain": "Python integers",
        "documented_examples": [15, 32],
        "empty_numeric_boundary": 0,
        "branch_boundaries": [-2, -1, 0, 1, 2, 3],
        "input_count": len(inputs),
        "input_groups": {
            "documented_and_boundaries": [str(value) for value in documented_and_boundaries],
            "exhaustive_small": "all integers in [-2048, 2048]",
            "deterministic_generated": {
                "seed": 790079,
                "count": 1000,
                "bit_lengths": "[1, 1024]",
            },
        },
        "all_inputs": [str(value) for value in inputs],
        "edge_results": edge_results,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
