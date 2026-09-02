#!/usr/bin/env python3
"""Ground satisfying witnesses for the formal entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/120-maximum")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.maximum


def maximum_spec(values: list[int], k: int) -> list[int]:
    sorted_values = sorted(values)
    return sorted_values[len(values) - k :]


def main() -> None:
    canonical = load("canonical_witness", ROOT / "reference" / "canonical.py")
    generated = load("generated_witness", ROOT / "candidate" / "solution.py")
    witnesses = [
        ([-3, -4, 5], 2),
        ([5], 1),
        ([7, -1], 0),
    ]
    for values, k in witnesses:
        precondition = 0 <= k <= len(values)
        formal_result = maximum_spec(values, k)
        canonical_result = canonical(list(values), k)
        generated_result = generated(list(values), k)
        print(
            f"L={values} K={k} precondition={precondition} "
            f"maximumSpec={formal_result} canonical={canonical_result} "
            f"generated={generated_result} all_equal="
            f"{formal_result == canonical_result == generated_result}"
        )
        if not precondition or formal_result != canonical_result or formal_result != generated_result:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
