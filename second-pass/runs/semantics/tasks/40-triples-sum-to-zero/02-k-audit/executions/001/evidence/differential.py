#!/usr/bin/env python3
"""Independent differential check of candidate and trusted canonical entry points."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


TRUSTED_PATH = Path("/tmp/audit-work/forty-triples-audit/trusted/canonical.py")
CANDIDATE_PATH = Path(
    "/tmp/audit-work/forty-triples-audit/candidate-src/solution.py"
)
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.json")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    trusted = load(TRUSTED_PATH, "trusted_canonical")
    candidate = load(CANDIDATE_PATH, "candidate_solution")

    named = [
        ("doc-1", [1, 3, 5, 0]),
        ("doc-2", [1, 3, -2, 1]),
        ("doc-3", [1, 2, 3, 7]),
        ("doc-4", [2, 4, -5, 3, 9, 7]),
        ("doc-5", [1]),
        ("empty", []),
        ("length-2-zeroes", [0, 0]),
        ("length-3-true", [0, 0, 0]),
        ("length-3-false", [-1, 0, 2]),
        ("first-triple-true", [-3, 1, 2, 50, 60]),
        ("last-triple-true", [50, 60, -3, 1, 2]),
        ("same-value-distinct-indices", [2, 2, -4]),
        ("one-zero-not-three", [0, 1, 2, 3]),
        ("length-7-beyond-proof", [9, 8, 7, 6, -5, 2, 3]),
        ("large-integers", [10**80, -(10**80), 0]),
    ]

    exhaustive = [
        list(values)
        for length in range(7)
        for values in itertools.product(range(-3, 4), repeat=length)
    ]

    rng = random.Random(400024)
    generated = [
        [rng.randint(-20, 20) for _ in range(rng.randint(0, 14))]
        for _ in range(4000)
    ]

    ordered_inputs = [values for _, values in named] + exhaustive + generated
    INPUTS_PATH.write_text(
        json.dumps(
            {
                "named": [{"name": name, "input": values} for name, values in named],
                "exhaustive_domain": {
                    "lengths": [0, 1, 2, 3, 4, 5, 6],
                    "values": [-3, -2, -1, 0, 1, 2, 3],
                    "count": len(exhaustive),
                },
                "generated": {
                    "seed": 400024,
                    "count": len(generated),
                    "length_range": [0, 14],
                    "value_range": [-20, 20],
                    "inputs": generated,
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    true_count = 0
    false_count = 0
    for index, values in enumerate(ordered_inputs):
        expected = trusted.triples_sum_to_zero(list(values))
        actual = candidate.triples_sum_to_zero(list(values))
        if expected:
            true_count += 1
        else:
            false_count += 1
        if type(actual) is not bool or actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": values,
                    "trusted": expected,
                    "candidate": actual,
                    "candidate_type": type(actual).__name__,
                }
            )
            if len(mismatches) >= 20:
                break

    digest = hashlib.sha256(INPUTS_PATH.read_bytes()).hexdigest()
    for name, values in named:
        expected = trusted.triples_sum_to_zero(list(values))
        actual = candidate.triples_sum_to_zero(list(values))
        print(f"NAMED {name}: input={values!r} trusted={expected} candidate={actual}")
    print(f"INPUTS_SHA256 {digest}")
    print(f"NAMED_COUNT {len(named)}")
    print(f"EXHAUSTIVE_COUNT {len(exhaustive)}")
    print(f"GENERATED_COUNT {len(generated)}")
    print(f"TOTAL_COMPARISONS {len(ordered_inputs)}")
    print(f"TRUSTED_TRUE_COUNT {true_count}")
    print(f"TRUSTED_FALSE_COUNT {false_count}")
    print(f"MISMATCH_COUNT {len(mismatches)}")
    for mismatch in mismatches:
        print("MISMATCH " + json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
