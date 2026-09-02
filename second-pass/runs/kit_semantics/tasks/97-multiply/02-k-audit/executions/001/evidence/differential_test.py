#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py versus solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


CANONICAL = Path("/reference/canonical.py")
SOLUTION = Path("/candidate/solution.py")


def load_function(module_name: str, path: Path):
    specification = importlib.util.spec_from_file_location(module_name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module.multiply


def outcome(function, a: int, b: int):
    try:
        value = function(a, b)
    except BaseException as error:  # Preserve exception class and message.
        return ("exception", type(error).__qualname__, str(error))
    return ("value", type(value).__qualname__, value)


def build_inputs() -> list[tuple[int, int]]:
    documented = [(148, 412), (19, 28), (2020, 1851), (14, -15)]
    zero_and_sign_boundaries = [
        (0, 0),
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
        (9, 9),
        (9, 10),
        (10, 9),
        (10, 10),
        (-9, 9),
        (-10, 9),
        (-11, 9),
        (9, -9),
        (9, -10),
        (9, -11),
    ]
    residue_cross_product = [
        (a, b) for a in range(-21, 22) for b in range(-21, 22)
    ]
    huge = 10**1000
    huge_boundaries = [
        (sign_a * huge + delta_a, sign_b * huge + delta_b)
        for sign_a in (-1, 1)
        for sign_b in (-1, 1)
        for delta_a in (-11, -10, -9, -1, 0, 1, 9, 10, 11)
        for delta_b in (-11, -10, -9, -1, 0, 1, 9, 10, 11)
    ]
    generator = random.Random(97002026)
    random_pairs = [
        (
            generator.randrange(-(10**150), 10**150),
            generator.randrange(-(10**150), 10**150),
        )
        for _ in range(1000)
    ]
    return documented + zero_and_sign_boundaries + residue_cross_product + huge_boundaries + random_pairs


def main() -> int:
    canonical = load_function("trusted_canonical_97", CANONICAL)
    solution = load_function("candidate_solution_97", SOLUTION)
    inputs = build_inputs()
    encoded_inputs = json.dumps(inputs, separators=(",", ":")).encode()
    mismatches = []
    for a, b in inputs:
        expected = outcome(canonical, a, b)
        actual = outcome(solution, a, b)
        if expected != actual:
            mismatches.append((a, b, expected, actual))

    print("oracle=/reference/canonical.py:multiply")
    print("subject=/candidate/solution.py:multiply")
    print("documented_examples=4")
    print("empty_cases=not_applicable_to_two_integer_parameters")
    print("control_flow_branches=none")
    print("residue_cross_product=[-21,21]^2")
    print("huge_boundaries=10**1000 plus offsets around multiples of ten")
    print("random_seed=97002026 random_pairs=1000 magnitude_bound=10**150")
    print(f"input_count={len(inputs)}")
    print(f"inputs_json_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
