#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path


sys.dont_write_bytecode = True
CANONICAL_PATH = Path("/tmp/audit-work/reconstruction/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/reconstruction/candidate-src/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential-inputs.json")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.car_race_collision


def main() -> int:
    canonical = load_function("trusted_canonical", CANONICAL_PATH)
    generated = load_function("submitted_solution", GENERATED_PATH)

    # The prompt contains no literal examples. These cover the empty population,
    # the first positive cardinality, candidate smoke values, large boundaries,
    # and deterministic representative nonnegative car counts.
    fixed_intended = [0, 1, 2, 3, 10, 50, 100, 1000, 2**31 - 1]
    rng = random.Random(410041)
    generated_intended = [rng.randrange(0, 1_000_001) for _ in range(500)]

    # Negative integers are outside the natural car-count interpretation but
    # exercise the stronger all-Int K claim's concrete Python counterpart.
    formal_scope_probes = [-1, -2, -10, -(2**31)]
    all_inputs = fixed_intended + generated_intended + formal_scope_probes
    INPUT_RECORD.write_text(
        json.dumps(
            {
                "seed": 410041,
                "fixed_intended": fixed_intended,
                "generated_intended": generated_intended,
                "formal_scope_probes": formal_scope_probes,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for n in all_inputs:
        expected = canonical(n)
        actual = generated(n)
        if type(actual) is not type(expected) or actual != expected:
            mismatches.append(
                {
                    "n": n,
                    "canonical": repr(expected),
                    "generated": repr(actual),
                    "canonical_type": type(expected).__name__,
                    "generated_type": type(actual).__name__,
                }
            )

    print(f"canonical_path={CANONICAL_PATH}")
    print(f"generated_path={GENERATED_PATH}")
    print("documented_example_count=0")
    print(f"intended_domain_case_count={len(fixed_intended) + len(generated_intended)}")
    print(f"formal_scope_probe_count={len(formal_scope_probes)}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2))
        return 1
    print("RESULT: all generated outputs matched the trusted canonical entry point")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
