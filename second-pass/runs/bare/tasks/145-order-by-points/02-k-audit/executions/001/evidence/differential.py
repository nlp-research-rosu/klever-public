#!/usr/bin/env python3
"""Independent differential test for HumanEval 145.

Oracle: /reference/canonical.py, loaded directly from the trusted mount.
Candidate: the freshly copied /tmp/audit-work/proof145/solution.py.

Input scope:
* the two documented examples;
* explicit empty, singleton, sign, decimal-boundary, tie, duplicate, and
  arbitrary-precision cases;
* every list of length 0..3 over a fixed boundary-heavy 17-value alphabet;
* 1,000 deterministic generated lists of length 0..12.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.order_by_points


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-out", type=Path, required=True)
    parser.add_argument("--results-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
    candidate = load_function(
        Path("/tmp/audit-work/proof145/solution.py"), "fresh_candidate"
    )

    cases: list[list[int]] = [
        [1, 11, -1, -11, -12],
        [],
        [0],
        [-1],
        [1],
        [-9, -10, -11, -12, -19, -20, -99, -100, -101],
        [9, 10, 11, 19, 20, 99, 100, 101],
        [12, 21, -12, 3],
        [11, 2, 20, 101, -11, -2, -20, -101],
        [0, 0, -1, -1, 1, 1],
        [10**80 + 23, -(10**80 + 23), 10**80, -(10**80)],
    ]

    alphabet = [-101, -100, -99, -20, -12, -11, -10, -1, 0,
                1, 2, 9, 10, 11, 12, 20, 101]
    for length in range(4):
        cases.extend([list(values) for values in itertools.product(alphabet, repeat=length)])

    rng = random.Random(145)
    for _ in range(1000):
        length = rng.randrange(13)
        row = []
        for _ in range(length):
            selector = rng.randrange(5)
            if selector == 0:
                row.append(rng.choice(alphabet))
            elif selector == 1:
                row.append(rng.randrange(-10**6, 10**6 + 1))
            elif selector == 2:
                row.append(rng.randrange(-10**30, 10**30 + 1))
            elif selector == 3:
                digits = rng.randrange(1, 121)
                magnitude = rng.randrange(10 ** (digits - 1), 10**digits)
                row.append(magnitude if rng.randrange(2) else -magnitude)
            else:
                row.append(0)
        cases.append(row)

    args.inputs_out.write_text(
        json.dumps(
            {
                "oracle": "/reference/canonical.py",
                "candidate": "/tmp/audit-work/proof145/solution.py",
                "scope": __doc__,
                "cases": cases,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    digest = hashlib.sha256()
    for index, values in enumerate(cases):
        oracle_input = list(values)
        candidate_input = list(values)
        expected = canonical(oracle_input)
        actual = candidate(candidate_input)
        record = {"index": index, "input": values, "expected": expected, "actual": actual}
        digest.update(json.dumps(record, sort_keys=True).encode())
        if actual != expected or oracle_input != values or candidate_input != values:
            mismatches.append(record)
            if len(mismatches) >= 20:
                break

    documented_expected = [-1, -11, 1, -12, 11]
    documented_actual = candidate([1, 11, -1, -11, -12])
    if documented_actual != documented_expected:
        mismatches.append(
            {
                "kind": "documented-expected",
                "expected": documented_expected,
                "actual": documented_actual,
            }
        )

    results = {
        "case_count": len(cases),
        "mismatch_count": len(mismatches),
        "record_sha256": digest.hexdigest(),
        "documented_example_result": documented_actual,
        "empty_result": candidate([]),
        "mismatches": mismatches,
    }
    args.results_out.write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
