#!/usr/bin/env python3
"""Independent differential test for HumanEval 37 sort_even.

The corpus is deterministic and is serialized in full to the path supplied as
the third argument.  The oracle and subject modules are loaded from distinct
files without importing one another.
"""

from __future__ import annotations

import copy
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


def observed_call(function, value):
    argument = copy.deepcopy(value)
    try:
        result = function(argument)
        outcome = ("return", result)
    except Exception as error:  # This is part of the differential observation.
        outcome = ("raise", type(error).__name__, str(error))
    return outcome, argument


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: differential_test.py CANONICAL.py SOLUTION.py INPUTS.json"
        )

    canonical_path = Path(sys.argv[1]).resolve()
    solution_path = Path(sys.argv[2]).resolve()
    inputs_path = Path(sys.argv[3]).resolve()
    oracle = load_entry(canonical_path, "trusted_canonical_sort_even")
    subject = load_entry(solution_path, "scratch_generated_sort_even")

    documented_examples = [
        [1, 2, 3],
        [5, 6, 3, 4],
    ]
    branch_and_boundary_cases = [
        [],
        [7],
        [2, 1],
        [3, 1, 2],
        [4, 40, 3, 30, 2, 20, 1],
        [9, -1, 3, -2, 3, -3, 0],
        [0, 0, 0, 0],
        [-1, 8, -1, 7, -2, 6],
        [10**30, -10**30, 0, 1, -(10**30), 2],
    ]

    alphabet = [-2, -1, 0, 1, 2]
    exhaustive_small = [
        list(values)
        for length in range(0, 7)
        for values in itertools.product(alphabet, repeat=length)
    ]

    rng = random.Random(370037)
    generated = [
        [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 40))]
        for _ in range(512)
    ]

    cases = documented_examples + branch_and_boundary_cases + exhaustive_small + generated
    inputs_path.write_text(
        json.dumps(
            {
                "documented_examples": documented_examples,
                "branch_and_boundary_cases": branch_and_boundary_cases,
                "exhaustive_small": {
                    "alphabet": alphabet,
                    "lengths": [0, 1, 2, 3, 4, 5, 6],
                    "cases": exhaustive_small,
                },
                "generated": {
                    "seed": 370037,
                    "count": len(generated),
                    "length_range": [0, 40],
                    "value_range": [-1000, 1000],
                    "cases": generated,
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for index, case in enumerate(cases):
        oracle_outcome, oracle_argument_after = observed_call(oracle, case)
        subject_outcome, subject_argument_after = observed_call(subject, case)
        if (
            oracle_outcome != subject_outcome
            or oracle_argument_after != subject_argument_after
        ):
            mismatches.append(
                {
                    "index": index,
                    "input": case,
                    "oracle_outcome": oracle_outcome,
                    "subject_outcome": subject_outcome,
                    "oracle_argument_after": oracle_argument_after,
                    "subject_argument_after": subject_argument_after,
                }
            )
            if len(mismatches) >= 20:
                break

    print(f"oracle={canonical_path}")
    print(f"subject={solution_path}")
    print(f"documented_examples={len(documented_examples)}")
    print(f"branch_and_boundary_cases={len(branch_and_boundary_cases)}")
    print(f"exhaustive_small_cases={len(exhaustive_small)}")
    print(f"generated_seed=370037")
    print(f"generated_cases={len(generated)}")
    print(f"total_executions_per_implementation={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, default=repr))
        return 1
    print("RESULT: zero differential or input-mutation mismatches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
