#!/usr/bin/env python3
"""Independent differential and property checks for HumanEval/100."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_a_pile


def expected(n: int) -> list[int]:
    # Independent direct characterization of the prompt.
    return [n + 2 * level for level in range(n)]


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 2

    canonical = load_function(Path(sys.argv[1]), "trusted_canonical")
    candidate = load_function(Path(sys.argv[2]), "generated_solution")

    # Includes the documented example, the positive-domain boundary, both sides
    # of the loop guard at entry, small exhaustive values, parity representatives,
    # and larger deterministic samples. Zero and -1 are explicitly out of the
    # stated positive-integer domain but exercise empty-loop behavior.
    inputs = sorted(
        set([-1, 0, 1, 2, 3, 4, 5, 6, *range(1, 65), 99, 100, 257, 1000])
    )
    mismatches = 0

    for n in inputs:
        want = expected(n)
        canonical_result = canonical(n)
        candidate_result = candidate(n)
        ok = canonical_result == candidate_result == want
        if n > 0:
            ok = (
                ok
                and len(candidate_result) == n
                and candidate_result[0] == n
                and candidate_result[-1] == 3 * n - 2
                and all(
                    candidate_result[index + 1] - candidate_result[index] == 2
                    for index in range(n - 1)
                )
            )
        if not ok:
            mismatches += 1
        print(
            f"n={n} len={len(candidate_result)} "
            f"first={candidate_result[0] if candidate_result else None} "
            f"last={candidate_result[-1] if candidate_result else None} ok={ok}"
        )

    print(f"TESTED_INPUTS={inputs}")
    print(f"MISMATCHES={mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
