#!/usr/bin/env python3
"""Independent canonical-versus-submission differential test for HumanEval/31."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/reference/canonical.py")
SUBMISSION_PATH = Path("/tmp/audit-work/31-is-prime/solution.py")
SEED = 31031


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


def input_corpus() -> tuple[list[int], dict[str, list[int]]]:
    groups = {
        # Prompt examples.
        "documented_examples": [6, 101, 11, 13441, 61, 4, 1],
        # Scalar task: n=0 is the empty candidate-divisor interval. The remaining
        # values cross the n<2 branch and the first loop-entry boundary.
        "empty_and_entry_boundaries": [-10, -1, 0, 1, 2, 3, 4, 5],
        # Exercise guard equality at perfect squares, an immediate divisor, later
        # divisors, non-divisor loop iterations, and final true return.
        "branch_boundaries": [
            4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 21, 25, 26, 29,
            31, 35, 47, 49, 50, 77, 97, 121, 127, 169, 221, 289,
        ],
        "exhaustive_small_interval": list(range(-50, 501)),
    }
    rng = random.Random(SEED)
    groups["deterministic_generated_inputs"] = [
        rng.randint(-1000, 20000) for _ in range(300)
    ]

    ordered_unique = list(dict.fromkeys(n for group in groups.values() for n in group))
    return ordered_unique, groups


def main() -> int:
    canonical = load_entry("trusted_canonical_31", CANONICAL_PATH)
    submission = load_entry("submitted_solution_31", SUBMISSION_PATH)
    inputs, groups = input_corpus()
    records = []
    mismatches = []

    for n in inputs:
        expected = canonical(n)
        actual = submission(n)
        record = {"n": n, "canonical": expected, "submission": actual}
        records.append(record)
        if type(actual) is not type(expected) or actual != expected:
            mismatches.append(record)

    inputs_path = EVIDENCE / "differential-inputs.json"
    results_path = EVIDENCE / "differential-results.json"
    inputs_path.write_text(
        json.dumps(
            {
                "oracle": str(CANONICAL_PATH),
                "submission": str(SUBMISSION_PATH),
                "seed": SEED,
                "groups": groups,
                "ordered_unique_inputs": inputs,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    results_path.write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    digest = hashlib.sha256(results_path.read_bytes()).hexdigest()
    print(f"canonical={CANONICAL_PATH}")
    print(f"submission={SUBMISSION_PATH}")
    print(f"seed={SEED}")
    print(f"unique_input_count={len(inputs)}")
    print(f"results_sha256={digest}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
