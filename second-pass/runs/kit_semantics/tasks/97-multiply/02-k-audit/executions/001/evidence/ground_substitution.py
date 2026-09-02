#!/usr/bin/env python3
"""Concrete satisfying substitutions for the guard-free symbolic entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module.multiply


def main() -> int:
    canonical = load("canonical_ground", Path("/reference/canonical.py"))
    candidate = load("candidate_ground", Path("/candidate/solution.py"))
    witnesses = [
        (148, 412),
        (14, -15),
        (-14, 15),
        (-11, -19),
        (0, 0),
        (10**250 + 7, -(10**250) - 3),
    ]
    mismatch_count = 0
    for a, b in witnesses:
        claimed = (a % 10) * (b % 10)
        canonical_value = canonical(a, b)
        candidate_value = candidate(a, b)
        agrees = claimed == canonical_value == candidate_value
        mismatch_count += not agrees
        print(
            f"A={a} B={b} claimed={claimed} "
            f"canonical={canonical_value} candidate={candidate_value} agrees={agrees}"
        )
    print(f"satisfying_entry_states={len(witnesses)}")
    print(f"mismatch_count={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
