#!/usr/bin/env python3
"""Differential boundary probe for unbounded prompt strings vs CPython recursion."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def outcome(function, word: str):
    try:
        return ("return", function(word))
    except BaseException as error:  # The exception itself is the observed mismatch.
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    canonical = load_entry("trusted_canonical_long", Path("/reference/canonical.py"))
    candidate = load_entry(
        "scratch_candidate_long", Path("/tmp/audit-work/candidate-src/solution.py")
    )
    inputs = [
        "b" * 990,
        "b" * 1000,
        "b" * 1100,
        "b" * 1500,
        "b" * 1497 + "bAb",  # immediate success avoids deep recursion
    ]
    mismatches = 0
    for word in inputs:
        canonical_outcome = outcome(canonical, word)
        candidate_outcome = outcome(candidate, word)
        mismatch = canonical_outcome != candidate_outcome
        mismatches += int(mismatch)
        print(
            f"length={len(word)} suffix={word[-8:]!r} "
            f"canonical={canonical_outcome!r} candidate={candidate_outcome!r} "
            f"mismatch={mismatch}"
        )
    print(f"TOTAL_INPUTS: {len(inputs)}")
    print(f"MISMATCHES: {mismatches}")
    # This audit probe is expected to expose at least one mismatch.
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
