#!/usr/bin/env python3
"""Independent differential test of the candidate and trusted Python functions."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.circular_shift


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: differential_test.py SCRATCH_DIRECTORY")
    scratch = Path(sys.argv[1])
    candidate = load_function(scratch / "solution.py", "candidate_solution")
    canonical = load_function(scratch / "trusted-canonical.py", "trusted_canonical")

    documented = [(12, 1), (12, 2)]
    boundary: list[tuple[int, int]] = []
    x_values = [
        -(10**40 + 123456789),
        -1234,
        -100,
        -10,
        -1,
        0,
        1,
        9,
        10,
        12,
        99,
        100,
        1234,
        10**40 + 987654321,
    ]
    for x in x_values:
        width = len(str(x))
        for shift in sorted(
            {-100, -10, -2, -1, 0, 1, width - 1, width, width + 1, width + 2, 100}
        ):
            boundary.append((x, shift))

    rng = random.Random(650026)
    generated = [
        (rng.randint(-(10**80), 10**80), rng.randint(-160, 240))
        for _ in range(2000)
    ]
    cases = documented + boundary + generated

    mismatches: list[tuple[int, int, str, str]] = []
    for x, shift in cases:
        expected = canonical(x, shift)
        actual = candidate(x, shift)
        if actual != expected:
            mismatches.append((x, shift, expected, actual))

    print("oracle", scratch / "trusted-canonical.py")
    print("candidate", scratch / "solution.py")
    print("documented_cases", len(documented))
    print("boundary_cases", len(boundary))
    print("generated_cases", len(generated))
    print("total_cases", len(cases))
    print("negative_shift_cases", sum(shift < 0 for _, shift in cases))
    print("zero_shift_cases", sum(shift == 0 for _, shift in cases))
    print(
        "equal_length_boundary_cases",
        sum(shift == len(str(x)) for x, shift in cases),
    )
    print(
        "oversized_branch_cases",
        sum(shift > len(str(x)) for x, shift in cases),
    )
    print("sample_negative", [(x, s, canonical(x, s)) for x, s in [(1234, -1), (0, -1)]])
    print("mismatch_count", len(mismatches))
    for mismatch in mismatches[:20]:
        print("MISMATCH", mismatch)
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
