#!/usr/bin/env python3
"""Independent differential tests for HumanEval 77 (iscube)."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random


WORK = Path("/tmp/audit-work/rebuild")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.iscube


def exact_iscube(value: int) -> bool:
    magnitude = abs(value)
    low, high = 0, 1
    while high * high * high < magnitude:
        high *= 2
    while low <= high:
        middle = (low + high) // 2
        cube = middle * middle * middle
        if cube == magnitude:
            return True
        if cube < magnitude:
            low = middle + 1
        else:
            high = middle - 1
    return False


def main() -> None:
    canonical = load_entry("trusted_canonical", WORK / "trusted_canonical.py")
    generated = load_entry("generated_solution", WORK / "solution.py")

    documented_examples = [1, 2, -1, 64, 0, 180]
    branch_boundaries = [-2, -1, 0, 1, 2]

    cube_boundaries: list[int] = []
    for root in list(range(0, 41)) + [100, 1000, 10_000, 100_000]:
        cube = root**3
        for delta in (-1, 0, 1):
            if cube + delta >= 0:
                cube_boundaries.extend([cube + delta, -(cube + delta)])

    exhaustive_small = list(range(-5_000, 5_001))
    generator = random.Random(770077)
    deterministic_generated = [
        generator.randint(-1_000_000, 1_000_000) for _ in range(2_000)
    ]

    # Preserve order while deduplicating.
    inputs = list(
        dict.fromkeys(
            documented_examples
            + branch_boundaries
            + cube_boundaries
            + exhaustive_small
            + deterministic_generated
        )
    )

    mismatches: list[tuple[int, bool, bool, bool]] = []
    for value in inputs:
        expected = exact_iscube(value)
        canonical_result = canonical(value)
        generated_result = generated(value)
        if canonical_result != expected or generated_result != expected:
            mismatches.append(
                (value, canonical_result, generated_result, expected)
            )

    print("contract_domain=valid Python integers; scalar input has no empty case")
    print(f"documented_examples={documented_examples}")
    print(f"branch_boundaries={branch_boundaries}")
    print("cube_boundary_roots=0..40,100,1000,10000,100000; deltas=-1,0,1; both signs")
    print("exhaustive_small=-5000..5000")
    print("deterministic_generated=count=2000 seed=770077 range=[-1000000,1000000]")
    print(f"unique_inputs={len(inputs)}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(
            "MISMATCH value={} canonical={} generated={} exact={}".format(
                *mismatch
            )
        )
    if mismatches:
        raise SystemExit(1)
    print("DIFFERENTIAL_TEST: PASS")


if __name__ == "__main__":
    main()
