#!/usr/bin/env python3
"""Independent differential check for HumanEval problem 75.

The trusted canonical and submitted generated entry points are imported from
separate filesystem paths.  The arithmetic oracle is independently implemented
and is used only as additional finite evidence.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/75-prime")


def import_from_path(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exactly_three_prime_factors_with_multiplicity(value: int) -> bool:
    """Independent trial-division oracle for the prompt/canonical behavior."""
    if value < 2:
        return False
    remaining = value
    count = 0
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            remaining //= divisor
            count += 1
        divisor += 1
    if remaining > 1:
        count += 1
    return count == 3


def main() -> int:
    canonical = import_from_path(
        "trusted_canonical", SCRATCH / "trusted" / "canonical.py"
    )
    generated = import_from_path(
        "submitted_generated", SCRATCH / "candidate" / "solution.py"
    )

    # The intended integer domain is a < 100.  This exhausts -64..99, includes
    # the example 30 and all small control-flow/factorization boundaries, and
    # adds representative points from the unbounded negative tail.
    inputs = list(range(-64, 100)) + [-100, -101, -1_000, -1_000_000]
    inputs = sorted(set(inputs))

    records = []
    mismatches = []
    accepted = []
    for value in inputs:
        canonical_result = canonical.is_multiply_prime(value)
        generated_result = generated.is_multiply_prime(value)
        arithmetic_result = exactly_three_prime_factors_with_multiplicity(value)
        record = {
            "input": value,
            "canonical": canonical_result,
            "generated": generated_result,
            "arithmetic_oracle": arithmetic_result,
        }
        records.append(record)
        if canonical_result:
            accepted.append(value)
        if not (
            canonical_result == generated_result == arithmetic_result
            and type(canonical_result) is bool
            and type(generated_result) is bool
        ):
            mismatches.append(record)

    report = {
        "scope": (
            "all integers -64..99 plus -100, -101, -1000, and -1000000; "
            "the scalar-integer contract has no empty-input case"
        ),
        "input_count": len(inputs),
        "inputs": inputs,
        "accepted_inputs": accepted,
        "documented_example_30": next(r for r in records if r["input"] == 30),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
