#!/usr/bin/env python3
"""Independent differential test for HumanEval 163.

The oracle is /tmp/audit-work/submitted/canonical.py, copied verbatim from the
trusted /reference/canonical.py.  The implementation under test is the copied
candidate solution.py.  The test generator does not reuse verification.k or its
evenDigits equations.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    oracle = load_function(args.workdir / "canonical.py", "trusted_canonical")
    generated = load_function(args.workdir / "solution.py", "candidate_solution")

    # Contract examples; empty intervals; exact even-digit points; both orders;
    # immediate neighbors of every branch threshold; and large positive values.
    named = [
        ("example-forward", 2, 8),
        ("example-reverse", 8, 2),
        ("example-empty-high", 10, 14),
        ("empty-low", 1, 1),
        ("all-digits-wide", 1, 9),
        ("middle", 3, 7),
        ("singleton-2", 2, 2),
        ("singleton-4", 4, 4),
        ("singleton-6", 6, 6),
        ("singleton-8", 8, 8),
        ("near-2-left", 1, 2),
        ("near-2-right", 2, 3),
        ("near-4-left", 3, 4),
        ("near-4-right", 4, 5),
        ("near-6-left", 5, 6),
        ("near-6-right", 6, 7),
        ("near-8-left", 7, 8),
        ("near-8-right", 8, 9),
        ("cross-no-even", 9, 10),
        ("reverse-middle", 7, 3),
        ("large", 10**12, 10**12 + 17),
        ("reverse-large-span", 10**12, 1),
    ]

    cases: list[dict[str, int | str]] = [
        {"kind": name, "a": a, "b": b} for name, a, b in named
    ]

    # Exhaustive small positive grid covers every truth combination at all four
    # threshold digits and both endpoint orders.
    for a in range(1, 65):
        for b in range(1, 65):
            cases.append({"kind": "grid-1..64", "a": a, "b": b})

    # Reproducible representative positive-domain sample beyond the small grid.
    rng = random.Random(163)
    for _ in range(500):
        cases.append(
            {
                "kind": "seeded-random-1..1000000",
                "a": rng.randint(1, 1_000_000),
                "b": rng.randint(1, 1_000_000),
            }
        )

    args.inputs_out.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

    mismatches = []
    for index, case in enumerate(cases):
        a = int(case["a"])
        b = int(case["b"])
        expected = oracle(a, b)
        actual = generated(a, b)
        if expected != actual:
            mismatches.append(
                {
                    "index": index,
                    "case": case,
                    "expected": expected,
                    "actual": actual,
                }
            )

    print("oracle=/reference/canonical.py (scratch copy)")
    print("implementation=/candidate/solution.py (scratch copy)")
    print(f"named_cases={len(named)}")
    print("exhaustive_grid=positive endpoints 1..64 x 1..64")
    print("random_sample=500 pairs, seed=163, endpoints 1..1000000")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
