#!/usr/bin/env python3
"""Ground witnesses for the universal reachability claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def main() -> int:
    canonical = load_entry(
        "canonical_claim_witness",
        Path("/tmp/audit-work/review-144/reference/canonical.py"),
    )
    generated = load_entry(
        "generated_claim_witness",
        Path("/tmp/audit-work/review-144/source/solution.py"),
    )
    witnesses = [
        ("minimum_true", 1, 1, 1, 1),
        ("prompt_false", 1, 6, 2, 1),
        ("cross_cancel_true", 2, 3, 3, 2),
        ("nonzero_remainder", 7, 10, 10, 2),
    ]
    failures = []
    for label, a, b, c, d in witnesses:
        precondition = a > 0 and b > 0 and c > 0 and d > 0
        claimed_result = ((a * c) % (b * d)) == 0
        x, n = f"{a}/{b}", f"{c}/{d}"
        canonical_result = canonical(x, n)
        generated_result = generated(x, n)
        print(
            f"{label}: A={a}, B={b}, C={c}, D={d}, "
            f"precondition={precondition}, claimed_result={claimed_result}, "
            f"canonical={canonical_result}, generated={generated_result}"
        )
        if not precondition or not (
            claimed_result == canonical_result == generated_result
        ):
            failures.append(label)
    print(f"witness_count={len(witnesses)}")
    print(f"failure_count={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
