#!/usr/bin/env python3
"""Independent candidate/canonical differential test for audit 46-fib4."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/46-fib4/solution.py")


def load_entry(module_name: str, path: Path) -> Callable[[int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


def outcome(fn: Callable[[int], int], n: int) -> dict[str, Any]:
    try:
        value = fn(n)
        return {"kind": "value", "type": type(value).__name__, "value": value}
    except Exception as err:  # The exception class is observable evidence.
        return {"kind": "exception", "type": type(err).__name__, "message": str(err)}


def main() -> int:
    canonical = load_entry("trusted_canonical", CANONICAL_PATH)
    generated = load_entry("scratch_generated", GENERATED_PATH)

    documented = [5, 6, 7]
    base_and_branches = list(range(0, 10))
    empty_loop_and_boundaries = [0, 1, 2, 3, 4, 5]
    rng = random.Random(4604)
    representative_generated = [rng.randrange(0, 1001) for _ in range(100)]
    intended_inputs = sorted(
        set(
            documented
            + base_and_branches
            + empty_loop_and_boundaries
            + list(range(0, 201))
            + representative_generated
        )
    )

    mismatches = []
    for n in intended_inputs:
        expected = outcome(canonical, n)
        actual = outcome(generated, n)
        if actual != expected:
            mismatches.append({"n": n, "canonical": expected, "generated": actual})

    # Negative integers are outside the sequence-index domain used by the proof.
    # Preserve their behavior to make that scope restriction visible.
    outside_domain = []
    for n in [-8, -5, -4, -3, -2, -1]:
        outside_domain.append(
            {
                "n": n,
                "canonical": outcome(canonical, n),
                "generated": outcome(generated, n),
            }
        )

    report = {
        "oracle": str(CANONICAL_PATH),
        "generated": str(GENERATED_PATH),
        "documented_examples": documented,
        "branch_boundary_inputs": empty_loop_and_boundaries,
        "representative_seed": 4604,
        "intended_domain": "integer n >= 0",
        "intended_inputs": intended_inputs,
        "intended_input_count": len(intended_inputs),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "outside_domain_characterization": outside_domain,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
