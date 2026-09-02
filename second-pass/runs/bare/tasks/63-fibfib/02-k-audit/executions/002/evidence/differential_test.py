#!/usr/bin/env python3
"""Independent contract/differential checks for HumanEval 63 (fibfib)."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/63-fibfib")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


def contract_oracle(n: int) -> int:
    """Directly iterate the recurrence from the trusted natural-language contract."""
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1
    f0, f1, f2 = 0, 0, 1
    for _ in range(3, n + 1):
        f0, f1, f2 = f1, f2, f0 + f1 + f2
    return f2


def describe_call(function, n: int) -> str:
    try:
        return f"value:{function(n)}"
    except BaseException as error:
        return f"exception:{type(error).__name__}"


def main() -> None:
    canonical = load_entry(ROOT / "reference" / "canonical.py", "trusted_canonical")
    generated = load_entry(ROOT / "candidate" / "solution.py", "generated_solution")

    documented = [1, 5, 8]
    branch_boundaries = [0, 1, 2, 3, 4]
    exhaustive_small = list(range(0, 21))
    rng = random.Random(630063)
    generated_sample = [rng.randrange(0, 21) for _ in range(64)]
    inputs = sorted(set(documented + branch_boundaries + exhaustive_small + generated_sample))

    mismatches = []
    for n in inputs:
        expected = contract_oracle(n)
        trusted = canonical(n)
        observed = generated(n)
        row = (n, expected, trusted, observed)
        print(f"n={n:2d} contract={expected} canonical={trusted} generated={observed}")
        if not (expected == trusted == observed):
            mismatches.append(row)

    large_rows = []
    for n in (25, 50, 100, 250):
        expected = contract_oracle(n)
        observed = generated(n)
        large_rows.append((n, expected, observed))
        print(f"large n={n} contract={expected} generated={observed}")
        if expected != observed:
            mismatches.append((n, expected, "not-run", observed))

    # The source contract describes sequence indices, hence n >= 0. This
    # diagnostic makes the excluded negative behavior explicit.
    print(
        "outside-domain n=-1 "
        f"canonical={describe_call(canonical, -1)} "
        f"generated={describe_call(generated, -1)}"
    )
    print("empty-case=N/A (the entry point accepts one integer, not a container)")
    print(
        f"SUMMARY compared={len(inputs)} small/distinct + {len(large_rows)} large "
        f"mismatches={len(mismatches)}"
    )
    assert mismatches == [], mismatches


if __name__ == "__main__":
    main()
