#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 146.

The oracle and candidate are loaded directly from their separate source files.
The corpus is deterministic and the complete concrete inputs are preserved as
JSON via --inputs-out.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.specialFilter


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_entry("generated_solution", Path("/candidate/solution.py"))

    cases: list[list[int]] = [
        [15, -73, 14, -15],
        [33, -2, -3, 45, 21, 109],
        [],
        [9, 10, 11],
        [11, 12, 13, 15, 19],
        [20, 21, 22, 29],
        [31, 33, 39, 40, 41, 49],
        [99, 100, 101, 109, 110, 111],
        [-1001, -99, -15, -11, -10, -3, -1, 0],
        [12],
        [15],
        [12, 15, 33],
        [10**30 + 1, 10**30 + 2, 9 * 10**40 + 9],
    ]

    # Exhaust every integer singleton around the threshold and all two-element
    # combinations of values chosen to hit both boolean branches and both
    # short-circuit outcomes.
    cases.extend([[n] for n in range(-250, 401)])
    boundary_values = [
        -15, -1, 0, 9, 10, 11, 12, 13, 15, 19, 20, 21, 22,
        31, 33, 45, 79, 99, 100, 101, 109, 110, 111, 9990, 13579,
    ]
    cases.extend([[a, b] for a in boundary_values for b in boundary_values])

    rng = random.Random(146)
    for _ in range(1000):
        length = rng.randrange(0, 21)
        cases.append([rng.randint(-1_000_000, 1_000_000) for _ in range(length)])

    encoded = json.dumps(cases, separators=(",", ":"), ensure_ascii=True)
    args.inputs_out.write_text(encoded + "\n", encoding="utf-8")

    mismatches = []
    for index, nums in enumerate(cases):
        expected = canonical(list(nums))
        actual = generated(list(nums))
        if actual != expected:
            mismatches.append(
                {"index": index, "input": nums, "canonical": expected, "generated": actual}
            )

    witnesses = {
        str(nums): {
            "canonical": canonical(list(nums)),
            "generated": generated(list(nums)),
        }
        for nums in ([12], [15], [12, 15, 33], [])
    }
    report = {
        "domain": "finite lists of Python integers",
        "case_count": len(cases),
        "input_sha256": hashlib.sha256((encoded + "\n").encode()).hexdigest(),
        "mismatch_count": len(mismatches),
        "first_mismatches": mismatches[:10],
        "satisfying_witnesses": witnesses,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
