#!/usr/bin/env python3
"""Ground interpretations of the formal postcondition for satisfying inputs."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


sys.dont_write_bytecode = True


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.by_length


def formal_postcondition_interpretation(values: list[int]) -> list[str]:
    # intVals is the identity embedding on integers.
    int_values = list(values)
    # filterDigits retains 1..9.
    filtered = [value for value in int_values if 1 <= value <= 9]
    # Supplied-semantics trust boundary: interpret sortVS as ascending sorted().
    ascending = sorted(filtered)
    # revVS then tableNames.
    descending = list(reversed(ascending))
    names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    return [names[value - 1] for value in descending]


def main() -> int:
    canonical = load("ground_canonical", Path("/reference/canonical.py"))
    generated = load(
        "ground_generated",
        Path("/tmp/audit-work/105-by-length/candidate/solution.py"),
    )
    cases = [
        [],
        [1],
        [0, 1, 9, 10],
        [2, 1, 1, 4, 5, 8, 2, 3],
    ]
    mismatches = 0
    for values in cases:
        claimed = formal_postcondition_interpretation(values)
        canonical_result = canonical(list(values))
        generated_result = generated(list(values))
        print(
            f"input={values!r} claimed={claimed!r} "
            f"canonical={canonical_result!r} generated={generated_result!r}"
        )
        if not (claimed == canonical_result == generated_result):
            mismatches += 1
    print(f"mismatch_count={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
