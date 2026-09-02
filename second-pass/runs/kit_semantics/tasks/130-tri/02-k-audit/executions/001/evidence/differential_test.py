#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.tri


def main() -> int:
    canonical = load_function("trusted_canonical", ROOT / "canonical.py")
    generated = load_function("generated_solution", ROOT / "solution.py")

    documented = {
        0: [1],
        1: [1, 3],
        2: [1, 3, 2],
        3: [1, 3, 2, 8],
        4: [1, 3, 2, 8, 3],
        5: [1, 3, 2, 8, 3, 15],
    }
    rng = random.Random(130)
    branch_and_dense = list(range(0, 257))
    representative = [rng.randrange(0, 2001) for _ in range(200)]
    large_boundaries = [511, 512, 513, 999, 1000, 1001, 4096, 10000]
    inputs = sorted(set(branch_and_dense + representative + large_boundaries))

    documented_mismatches = []
    semantic_mismatches = []
    type_differences = []
    for n in inputs:
        expected = documented.get(n)
        reference_result = canonical(n)
        generated_result = generated(n)
        if expected is not None:
            if reference_result != expected or generated_result != expected:
                documented_mismatches.append(
                    {
                        "n": n,
                        "expected": expected,
                        "canonical": reference_result,
                        "generated": generated_result,
                    }
                )
        if generated_result != reference_result:
            semantic_mismatches.append(
                {
                    "n": n,
                    "canonical": reference_result,
                    "generated": generated_result,
                }
            )
        reference_types = [type(value).__name__ for value in reference_result]
        generated_types = [type(value).__name__ for value in generated_result]
        if reference_types != generated_types:
            type_differences.append(
                {
                    "n": n,
                    "first_reference_types": reference_types[:6],
                    "first_generated_types": generated_types[:6],
                }
            )

    print(f"oracle=/tmp/audit-work/reconstruction/canonical.py::tri")
    print(f"subject=/tmp/audit-work/reconstruction/solution.py::tri")
    print("intended_domain=non-negative Python integers")
    print(
        "coverage=documented n=0..5; dense n=0..256; deterministic seed=130 "
        "sample of 200 values in 0..2000; large boundaries through 10000"
    )
    print("tested_inputs=" + json.dumps(inputs, separators=(",", ":")))
    print(f"tested_input_count={len(inputs)}")
    print(f"documented_mismatch_count={len(documented_mismatches)}")
    print(f"semantic_mismatch_count={len(semantic_mismatches)}")
    print(f"element_type_difference_input_count={len(type_differences)}")
    if documented_mismatches:
        print("documented_mismatches=" + json.dumps(documented_mismatches))
    if semantic_mismatches:
        print("semantic_mismatches=" + json.dumps(semantic_mismatches))
    if type_differences:
        print(
            "type_difference_note=trusted canonical uses / and therefore Python "
            "float elements from index 2 onward; generated program returns equal "
            "integer-valued elements via //; list equality and the numeric contract "
            "consider these equal"
        )
        print(
            "first_type_difference="
            + json.dumps(type_differences[0], separators=(",", ":"))
        )

    return 0 if not documented_mismatches and not semantic_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
