#!/usr/bin/env python3
"""Independent differential test of canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


def independent_oracle(values):
    output = []
    for value in values:
        if value > 0:
            output.append(value)
    return output


def main() -> int:
    canonical = load_entry(
        Path("/tmp/audit-work/30-get-positive/trusted/canonical.py"),
        "trusted_canonical",
    )
    candidate = load_entry(
        Path("/tmp/audit-work/30-get-positive/candidate-src/solution.py"),
        "generated_solution",
    )
    cases = [
        [-1, 2, -4, 5, 6],
        [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
        [],
        [-1],
        [0],
        [1],
        [-1, 0, 1],
        [1, 1, -1, 1],
        [-2.5, -0.0, 0.25, 3.5, 0.0],
        [float("-inf"), -1.0, 0.0, 1.0, float("inf")],
        [False, True, 0, 1, -1],
    ]
    boundary_pool = [-2, -1, 0, 1, 2]
    for length in range(5):
        cases.extend(list(values) for values in itertools.product(boundary_pool, repeat=length))
    rng = random.Random(20260726)
    for _ in range(1000):
        cases.append(
            [rng.randint(-10_000, 10_000) for _ in range(rng.randrange(0, 81))]
        )

    mismatches = []
    for index, values in enumerate(cases):
        expected = independent_oracle(values)
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        if canonical_result != expected or candidate_result != expected:
            mismatches.append(
                (index, values, expected, canonical_result, candidate_result)
            )
    print(
        "SCOPE "
        "2 documented examples; empty; singleton -1/0/+1; duplicate/order case; "
        "float, infinity, and bool cases; exhaustive lengths 0..4 over "
        "[-2,-1,0,1,2]; 1000 deterministic random integer lists "
        "(length 0..80, values -10000..10000)"
    )
    print(f"CASES={len(cases)} MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    # A concrete source-domain witness not representable by semantic.k's PyList.
    float_witness = [-1.5, 0.0, 2.25]
    print(
        "FLOAT_DOMAIN_WITNESS "
        f"input={float_witness!r} "
        f"canonical={canonical(float_witness)!r} "
        f"candidate={candidate(float_witness)!r} "
        "K_PyList_unrepresentable=True"
    )
    assert not math.isnan(float_witness[-1])
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
