#!/usr/bin/env python3
"""Independent differential test for HumanEval 24.

The trusted reference implementation and candidate implementation are loaded
from distinct files.  The in-domain suite combines the prompt example,
exhaustive small/boundary inputs, fixed branch-sensitive values, and
deterministically generated representative inputs.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


WORK = Path("/tmp/audit-work/24-largest-divisor")


def load_function(path: Path, module_name: str) -> Callable[[int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_divisor


def outcome(fn: Callable[[int], Any], value: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(value)}
    except Exception as error:  # Compare observable failure class, not wording.
        return {"kind": "exception", "type": type(error).__name__}


def main() -> int:
    canonical = load_function(WORK / "trusted-canonical.py", "trusted_canonical")
    generated = load_function(WORK / "solution.py", "generated_solution")

    documented = [15]
    exhaustive_small = list(range(2, 501))
    branch_sensitive = [
        2,  # loop guard is false immediately
        3,  # prime: loop decrements to 1
        4,  # one decrement, then divisor 2
        6, 8, 9, 10, 12, 16, 21, 25, 49,
        97, 101, 127, 997, 1024, 4096, 4999,
    ]
    rng = random.Random(240024)
    generated_inputs = [rng.randint(2, 5000) for _ in range(200)]
    in_domain = sorted(
        set(documented + exhaustive_small + branch_sensitive + generated_inputs)
    )

    mismatches = []
    for value in in_domain:
        expected = outcome(canonical, value)
        actual = outcome(generated, value)
        if expected != actual:
            mismatches.append(
                {"input": value, "canonical": expected, "candidate": actual}
            )

    # These are deliberately reported separately: the natural notion of a
    # positive proper divisor is undefined at n <= 1, and the K claim assumes
    # N > 1.
    outside_formal_domain = []
    for value in [0, 1]:
        outside_formal_domain.append(
            {
                "input": value,
                "canonical": outcome(canonical, value),
                "candidate": outcome(generated, value),
            }
        )

    report = {
        "oracle": str(WORK / "trusted-canonical.py"),
        "candidate": str(WORK / "solution.py"),
        "documented_inputs": documented,
        "exhaustive_small_range": [2, 500],
        "branch_sensitive_inputs": branch_sensitive,
        "generated_seed": 240024,
        "generated_draws": 200,
        "unique_in_domain_inputs": len(in_domain),
        "in_domain_mismatch_count": len(mismatches),
        "in_domain_mismatches": mismatches,
        "outside_formal_domain": outside_formal_domain,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
