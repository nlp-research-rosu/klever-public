#!/usr/bin/env python3
"""Independent differential check of the trusted and candidate Python entry points."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED_CANONICAL CANDIDATE_SOLUTION")
        return 64
    canonical = load_module("trusted_canonical", Path(sys.argv[1]))
    candidate = load_module("candidate_solution", Path(sys.argv[2]))

    documented = {1: 0, 5: 4, 8: 24}
    # 0 is the lower/zero-iteration boundary; 1 and 2 are the other base cases;
    # 3 crosses into the recurrence. 0..20 also exercises both loop branches
    # and a broader deterministic sample of the formal n >= 0 domain.
    inputs = list(range(0, 21))
    rows = []
    mismatches = 0
    for n in inputs:
        trusted_value = canonical.fibfib(n)
        candidate_value = candidate.fibfib(n)
        documented_value = documented.get(n)
        agrees = trusted_value == candidate_value
        example_agrees = (
            documented_value is None
            or (trusted_value == documented_value == candidate_value)
        )
        if not (agrees and example_agrees):
            mismatches += 1
        rows.append(
            {
                "n": n,
                "trusted": trusted_value,
                "candidate": candidate_value,
                "documented_expected": documented_value,
                "match": agrees and example_agrees,
            }
        )

    print(json.dumps(rows, indent=2, sort_keys=True))
    print(f"input_domain: integers n >= 0")
    print(f"tested_inputs: {inputs}")
    print(f"mismatch_count: {mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
