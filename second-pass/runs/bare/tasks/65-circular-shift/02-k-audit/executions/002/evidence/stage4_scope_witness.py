#!/usr/bin/env python3
"""Concrete witnesses for claim satisfiability and the uncovered source domain."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module.circular_shift


def predicates(x: int, shift: int) -> tuple[bool, bool]:
    length = len(str(x))
    normal_claim = 0 <= shift <= length
    oversized_claim = length < shift
    return normal_claim, oversized_claim


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: stage4_scope_witness.py SCRATCH_DIRECTORY")
    root = Path(sys.argv[1])
    candidate = load(root / "solution.py", "scope_candidate")
    canonical = load(root / "trusted-canonical.py", "scope_canonical")

    cases = [
        ("normal_precondition_witness", 12, 1),
        ("oversized_precondition_witness", 1234, 5),
        ("uncovered_negative_shift", 1234, -1),
        ("uncovered_negative_shift", 0, -1),
        ("uncovered_negative_shift", -1234, -3),
    ]
    for label, x, shift in cases:
        normal, oversized = predicates(x, shift)
        expected = canonical(x, shift)
        actual = candidate(x, shift)
        print(
            label,
            "x",
            x,
            "shift",
            shift,
            "normal_claim_precondition",
            normal,
            "oversized_claim_precondition",
            oversized,
            "canonical",
            repr(expected),
            "candidate",
            repr(actual),
        )
        if expected != actual:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
