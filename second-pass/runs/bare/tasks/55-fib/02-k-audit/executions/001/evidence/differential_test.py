#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval problem 55-fib."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib


def main() -> int:
    canonical = load_entry(
        "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
    )
    generated = load_entry(
        "submitted_solution", Path("/tmp/audit-work/src/solution.py")
    )

    documented = [10, 1, 8]
    boundaries = [0, 1, 2, 3]
    exhaustive_small = list(range(0, 21))
    rng = random.Random(550055)
    generated_inputs = [rng.randrange(0, 26) for _ in range(20)]
    representative_large = [25, 30]
    inputs = list(
        dict.fromkeys(
            documented
            + boundaries
            + exhaustive_small
            + generated_inputs
            + representative_large
        )
    )

    mismatches = []
    print(f"documented={documented}")
    print(f"boundaries={boundaries}")
    print(f"exhaustive_small={exhaustive_small}")
    print(f"generated_seed=550055 generated_inputs={generated_inputs}")
    print(f"representative_large={representative_large}")
    print("empty_case=not_applicable_to_scalar_integer_domain")
    for n in inputs:
        expected = canonical(n)
        actual = generated(n)
        print(f"n={n} canonical={expected} submitted={actual}")
        if actual != expected:
            mismatches.append((n, expected, actual))

    print(f"intended_domain_cases={len(inputs)} mismatches={len(mismatches)}")

    # Negative integers are outside the nonnegative domain on which the
    # canonical recursive definition terminates. Record, but do not count,
    # this implementation difference.
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(80)
    try:
        try:
            canonical_negative = canonical(-1)
            canonical_outcome = f"value:{canonical_negative}"
        except RecursionError:
            canonical_outcome = "RecursionError"
        try:
            submitted_negative = generated(-1)
            submitted_outcome = f"value:{submitted_negative}"
        except RecursionError:
            submitted_outcome = "RecursionError"
    finally:
        sys.setrecursionlimit(old_limit)
    print(
        "outside_domain_n=-1 "
        f"canonical={canonical_outcome} submitted={submitted_outcome}"
    )

    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
