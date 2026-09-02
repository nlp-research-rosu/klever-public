#!/usr/bin/env python3
"""Concrete witnesses for all three entry-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/116-sort-array")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


def popcount_abs(value: int) -> int:
    return abs(value).bit_count()


def main() -> int:
    canonical = load_function("stage4_canonical", SCRATCH / "canonical.py")
    candidate = load_function("stage4_candidate", SCRATCH / "solution.py")

    nonnegative = 5
    negative = -5
    print(
        "KEY_NONNEGATIVE_WITNESS "
        f"I={nonnegative} guard={nonnegative >= 0} "
        f"claimed_popcountAbs={popcount_abs(nonnegative)} "
        f"python_bin_count={bin(nonnegative).count('1')}"
    )
    print(
        "KEY_NEGATIVE_WITNESS "
        f"I={negative} guard={negative < 0} "
        f"claimed_popcountAbs={popcount_abs(negative)} "
        f"python_bin_count={bin(negative).count('1')}"
    )

    values = [3, 4, -2, 0]
    numeric_sort = sorted(values)
    claimed_interpretation = sorted(
        numeric_sort, key=lambda value: bin(value).count("1")
    )
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    print(
        "SORT_ARRAY_WITNESS "
        f"VS={values!r} allIntVS={all(type(value) is int for value in values)} "
        "initial_cells={env:0,scopeLoc:1,heapLoc:1,stack:empty,"
        "ret:noRet,exc:NoExc,exit:0}"
    )
    print(f"CLAIMED_SORTVS_INTERPRETATION={numeric_sort!r}")
    print(f"CLAIMED_SORTKEYVS_INTERPRETATION={claimed_interpretation!r}")
    print(f"TRUSTED_CANONICAL_RESULT={canonical_result!r}")
    print(f"CANDIDATE_PYTHON_RESULT={candidate_result!r}")
    equal = claimed_interpretation == canonical_result == candidate_result
    print(f"GROUND_RESULTS_EQUAL={equal}")
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
