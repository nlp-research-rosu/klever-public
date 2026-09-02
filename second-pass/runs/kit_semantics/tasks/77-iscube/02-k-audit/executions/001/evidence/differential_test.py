#!/usr/bin/env python3
"""Independent differential and contract-oracle test for HumanEval 77."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from types import ModuleType


CANONICAL_PATH = Path("/tmp/audit-work/reconstruction/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/candidate/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_cube_oracle(value: int) -> bool:
    """Binary-search exact cubeness; independent of both submitted algorithms."""
    magnitude = abs(value)
    low = 0
    high = 1
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
    canonical = load_module("trusted_canonical_77", CANONICAL_PATH)
    candidate = load_module("generated_candidate_77", CANDIDATE_PATH)

    documented = [1, 2, -1, 64, 0, 180]
    branch_boundaries = [
        -65,
        -64,
        -63,
        -28,
        -27,
        -26,
        -9,
        -8,
        -7,
        -2,
        -1,
        0,
        1,
        2,
        7,
        8,
        9,
        26,
        27,
        28,
        63,
        64,
        65,
    ]
    around_cubes: list[int] = []
    for root in range(0, 301):
        cube = root**3
        around_cubes.extend(
            [cube - 1, cube, cube + 1, -cube - 1, -cube, -cube + 1]
        )
    rng = random.Random(770077)
    generated = [rng.randint(-2_000_000, 2_000_000) for _ in range(2000)]
    larger_boundaries = []
    for root in [1000, 4096, 10000, 100000]:
        cube = root**3
        larger_boundaries.extend([cube - 1, cube, cube + 1, -cube])

    cases = sorted(
        set(
            documented
            + branch_boundaries
            + around_cubes
            + generated
            + larger_boundaries
        )
    )
    candidate_vs_canonical = []
    candidate_vs_contract = []
    canonical_vs_contract = []
    for value in cases:
        candidate_result = candidate.iscube(value)
        canonical_result = canonical.iscube(value)
        oracle_result = exact_cube_oracle(value)
        if candidate_result != canonical_result:
            candidate_vs_canonical.append(
                (value, candidate_result, canonical_result)
            )
        if candidate_result != oracle_result:
            candidate_vs_contract.append(
                (value, candidate_result, oracle_result)
            )
        if canonical_result != oracle_result:
            canonical_vs_contract.append(
                (value, canonical_result, oracle_result)
            )

    print(f"documented_examples={documented}")
    print("empty_case=not_applicable_to_integer_input")
    print(f"branch_boundary_count={len(set(branch_boundaries))}")
    print("generated_seed=770077")
    print("generated_range=-2000000..2000000")
    print(f"generated_count={len(generated)}")
    print(f"distinct_total_inputs={len(cases)}")
    print(
        f"candidate_vs_canonical_mismatches={len(candidate_vs_canonical)}"
    )
    print(f"candidate_vs_contract_mismatches={len(candidate_vs_contract)}")
    print(f"canonical_vs_contract_mismatches={len(canonical_vs_contract)}")
    if candidate_vs_canonical:
        print(f"candidate_vs_canonical_first={candidate_vs_canonical[:10]}")
    if candidate_vs_contract:
        print(f"candidate_vs_contract_first={candidate_vs_contract[:10]}")
    if canonical_vs_contract:
        print(f"canonical_vs_contract_first={canonical_vs_contract[:10]}")
    # The trusted canonical uses floating cube roots and ceases to implement
    # the literal prompt contract at very large roots. Running the candidate
    # here would require 10**15 loop iterations, so this is explicitly a
    # canonical-versus-contract probe, not a differential execution claim.
    huge_root = 10**15
    huge_cube = huge_root**3
    print(
        "canonical_large_exact_cube_probe="
        f"{canonical.iscube(huge_cube)} "
        f"contract_oracle={exact_cube_oracle(huge_cube)} "
        "candidate_execution=not_run"
    )
    if candidate_vs_canonical or candidate_vs_contract:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
