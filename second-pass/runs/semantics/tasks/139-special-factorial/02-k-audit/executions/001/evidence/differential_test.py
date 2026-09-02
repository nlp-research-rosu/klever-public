#!/usr/bin/env python3
"""Independent differential check for HumanEval problem 139.

Oracle: the trusted /reference/canonical.py entry point.
Subject: the scratch copy of the submitted /candidate/solution.py entry point.
"""

from __future__ import annotations

import hashlib
import importlib.util
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.special_factorial


def int_digest(value: int) -> str:
    size = max(1, (value.bit_length() + 8) // 8)
    payload = value.to_bytes(size, "big", signed=True)
    return hashlib.sha256(payload).hexdigest()[:16]


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical_139")
    generated = load_function(
        Path("/tmp/audit-work/139-special-factorial/solution.py"),
        "submitted_solution_139",
    )

    # "Empty" range and loop-entry boundaries are outside the stated n > 0
    # domain but expose the zero-iteration branch.  1 and 2 expose entry/exit
    # and a repeated iteration.  4 is the documented prompt example.
    named = {
        "negative_out_of_domain": -3,
        "negative_one_out_of_domain": -1,
        "empty_zero_out_of_domain": 0,
        "smallest_in_domain": 1,
        "second_iteration_boundary": 2,
        "documented_example": 4,
        "larger_small": 6,
        "medium": 25,
        "large": 100,
    }
    exhaustive_small = list(range(-5, 41))
    generator = random.Random(139_20260724)
    generated_inputs = [generator.randint(1, 160) for _ in range(40)]
    inputs = sorted(set(named.values()) | set(exhaustive_small) | set(generated_inputs))

    documented_expected = {1: 1, 2: 2, 3: 12, 4: 288, 5: 34560, 6: 24883200}
    mismatches = []
    expected_failures = []
    selected = {}
    for n in inputs:
        oracle_value = canonical(n)
        subject_value = generated(n)
        if oracle_value != subject_value:
            mismatches.append((n, oracle_value, subject_value))
        if n in documented_expected and subject_value != documented_expected[n]:
            expected_failures.append((n, documented_expected[n], subject_value))
        if n in named.values():
            selected[n] = {
                "bits": subject_value.bit_length(),
                "sha256_prefix": int_digest(subject_value),
            }

    print(f"named_cases={named}")
    print(f"exhaustive_small={exhaustive_small}")
    print(f"generated_seed=139_20260724")
    print(f"generated_inputs={generated_inputs}")
    print(f"unique_inputs={inputs}")
    print(f"documented_expected={documented_expected}")
    print(f"selected_result_metadata={selected}")
    print(f"differential_mismatches={len(mismatches)}")
    print(f"documented_expected_failures={len(expected_failures)}")
    if mismatches:
        print(f"mismatches={mismatches}")
    if expected_failures:
        print(f"expected_failures={expected_failures}")
    return 1 if mismatches or expected_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
