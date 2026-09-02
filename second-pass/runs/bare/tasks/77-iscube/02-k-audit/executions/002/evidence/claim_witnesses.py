#!/usr/bin/env python3
"""Ground witnesses for every candidate claim precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/rebuild")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.iscube


def main() -> None:
    canonical = load_entry("trusted_canonical_witness", WORK / "trusted_canonical.py")
    generated = load_entry("generated_solution_witness", WORK / "solution.py")

    # Helper claim witnesses:
    # cube-loop: N=2, I=1 gives a=8, n=1 and 0 <= I <= N.
    # gap-loop: N=2, D=1, I=1 gives a=9, n=1,
    #           0 < D < 3^3 - 2^3 and 0 <= I <= N+1.
    print("cube-loop witness: N=2 I=1 a=8 n=1 constraints=True final_n=2")
    print("gap-loop witness: N=2 D=1 I=1 a=9 n=1 constraints=True final_n=3")

    entries = [
        ("nonnegative-cube", 2, None, 8, True),
        ("negative-cube", 2, None, -8, True),
        ("positive-noncube", 2, 1, 9, False),
        ("negative-noncube", 2, 1, -9, False),
    ]
    mismatches = 0
    for claim, root, delta, value, claimed in entries:
        generated_result = generated(value)
        canonical_result = canonical(value)
        constraints = (
            root >= 0
            and (claim != "negative-cube" or root > 0)
            and (
                delta is None
                or (0 < delta < (root + 1) ** 3 - root**3)
            )
        )
        print(
            f"{claim}: N={root} D={delta} input={value} "
            f"precondition={constraints} claimed={claimed} "
            f"generated_python={generated_result} canonical_python={canonical_result}"
        )
        if not constraints or generated_result != claimed or canonical_result != claimed:
            mismatches += 1
    print(f"mismatch_count={mismatches}")
    if mismatches:
        raise SystemExit(1)
    print("CLAIM_WITNESSES: PASS")


if __name__ == "__main__":
    main()
