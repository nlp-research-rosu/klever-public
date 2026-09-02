#!/usr/bin/env python3
"""Independent canonical-versus-submitted differential test for count_up_to."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import random
import sys
from types import ModuleType


def load_module(name: str, path: pathlib.Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_prime_independent(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED_CANONICAL.py SUBMITTED_SOLUTION.py")
        return 64

    canonical_path = pathlib.Path(sys.argv[1]).resolve()
    submitted_path = pathlib.Path(sys.argv[2]).resolve()
    canonical = load_module("trusted_canonical", canonical_path)
    submitted = load_module("submitted_solution", submitted_path)

    documented = [5, 11, 0, 20, 1, 18]
    branch_boundaries = [
        2,   # outer loop zero iterations at candidate == n
        3,   # candidate 2, inner loop zero iterations
        4,   # candidate 3, inner loop zero iterations
        6,   # includes prime 5 but excludes boundary n
        9,   # composite 8; equality boundary follows at n=10
        10,  # perfect-square candidate 9 exercises D*D == C and divisor branch
        25,  # candidate 24 exercises non-divisor and later divisor paths
        26,  # perfect-square candidate 25 exercises divisor at sqrt boundary
        50,  # several composite and prime paths
    ]
    exhaustive = list(range(0, 301))
    rng = random.Random(960096)
    generated = [rng.randrange(0, 1001) for _ in range(64)]
    inputs = list(dict.fromkeys(documented + branch_boundaries + exhaustive + generated))

    encoded = json.dumps(inputs, separators=(",", ":")).encode("ascii")
    print(f"canonical={canonical_path}")
    print(f"submitted={submitted_path}")
    print(f"documented={json.dumps(documented)}")
    print(f"branch_boundaries={json.dumps(branch_boundaries)}")
    print("generated_seed=960096 generated_count=64 generated_range=[0,1000]")
    print(f"inputs_count={len(inputs)}")
    print(f"inputs_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"inputs_json={encoded.decode('ascii')}")

    expected_examples = {
        5: [2, 3],
        11: [2, 3, 5, 7],
        0: [],
        20: [2, 3, 5, 7, 11, 13, 17, 19],
        1: [],
        18: [2, 3, 5, 7, 11, 13, 17],
    }
    mismatches = []
    property_failures = []
    for n in inputs:
        reference_result = canonical.count_up_to(n)
        submitted_result = submitted.count_up_to(n)
        if reference_result != submitted_result:
            mismatches.append((n, reference_result, submitted_result))
        expected_property = [
            value for value in range(2, n) if is_prime_independent(value)
        ]
        if submitted_result != expected_property:
            property_failures.append((n, expected_property, submitted_result))
        if n in expected_examples and submitted_result != expected_examples[n]:
            property_failures.append(
                (f"documented:{n}", expected_examples[n], submitted_result)
            )

    for n in documented + branch_boundaries:
        print(
            "case "
            + json.dumps(
                {
                    "n": n,
                    "canonical": canonical.count_up_to(n),
                    "submitted": submitted.count_up_to(n),
                },
                separators=(",", ":"),
            )
        )

    print(f"mismatch_count={len(mismatches)}")
    print(f"property_failure_count={len(property_failures)}")
    if mismatches:
        print("mismatches=" + repr(mismatches[:20]))
    if property_failures:
        print("property_failures=" + repr(property_failures[:20]))
    return 1 if mismatches or property_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
