#!/usr/bin/env python3
"""Independent differential test: trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
from typing import Any, Callable


ROOT = Path("/tmp/audit-work/146-specialFilter")
INPUT_LOG = Path("/audit-output/evidence/differential-inputs.jsonl")


def load_function(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.specialFilter


def outcome(fn: Callable[[list[int]], int], nums: list[int]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(list(nums))}
    except Exception as error:  # Deliberately compare exception behavior too.
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}


def case_stream():
    fixed = [
        ("prompt-example-1", [15, -73, 14, -15]),
        ("prompt-example-2", [33, -2, -3, 45, 21, 109]),
        ("empty", []),
        ("threshold-boundary", [-999, -11, -1, 0, 1, 9, 10, 11, 12]),
        ("two-digit-parity-quadrants", [11, 12, 21, 22, 31, 42, 57, 68, 79, 90, 99]),
        ("digit-width-boundaries", [98, 99, 100, 101, 109, 110, 111, 998, 999, 1000, 1001, 1009, 1011]),
        ("wide-values", [10**20 + 1, 3 * 10**40 + 5, 8 * 10**50 + 7, -(10**30 + 11)]),
        ("repetition", [15, 15, 15, 20, 20]),
    ]
    yield from fixed

    for value in range(-2_000, 20_001):
        yield (f"singleton-{value}", [value])

    branch_values = [-73, -1, 0, 9, 10, 11, 12, 21, 22, 99, 100, 101, 109, 111, 313]
    for length in range(1, 4):
        for index, values in enumerate(itertools.product(branch_values, repeat=length)):
            yield (f"branch-product-{length}-{index}", list(values))

    generator = random.Random(146_20260723)
    for index in range(5_000):
        length = generator.randrange(0, 31)
        nums = [generator.randint(-(10**12), 10**12) for _ in range(length)]
        yield (f"random-{index}", nums)


def main() -> int:
    canonical = load_function(ROOT / "reference/canonical.py", "trusted_canonical")
    candidate = load_function(ROOT / "candidate/solution.py", "generated_solution")
    mismatches = []
    count = 0
    with INPUT_LOG.open("w", encoding="utf-8") as inputs:
        for label, nums in case_stream():
            count += 1
            inputs.write(json.dumps({"label": label, "nums": nums}, separators=(",", ":")) + "\n")
            expected = outcome(canonical, nums)
            actual = outcome(candidate, nums)
            if actual != expected:
                mismatches.append(
                    {"label": label, "nums": nums, "canonical": expected, "candidate": actual}
                )
                if len(mismatches) >= 20:
                    break

    digest = hashlib.sha256(INPUT_LOG.read_bytes()).hexdigest()
    print("oracle=/tmp/audit-work/146-specialFilter/reference/canonical.py:specialFilter")
    print("subject=/tmp/audit-work/146-specialFilter/candidate/solution.py:specialFilter")
    print("domain=finite lists of Python integers")
    print("fixed_cases=8")
    print("exhaustive_singletons=-2000..20000 inclusive")
    print("branch_cartesian_products=lengths 1..3 over 15 fixed boundary values")
    print("random_seed=14620260723")
    print("random_cases=5000, list lengths 0..30, values -10^12..10^12")
    print(f"executed_cases={count}")
    print(f"input_log={INPUT_LOG}")
    print(f"input_log_sha256={digest}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches:
            print(json.dumps(mismatch, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
