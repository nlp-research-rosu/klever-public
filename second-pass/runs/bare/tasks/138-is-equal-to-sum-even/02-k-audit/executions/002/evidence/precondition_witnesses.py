#!/usr/bin/env python3
"""Exhibit concrete satisfying states and evaluate the claimed results."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_equal_to_sum_even


def sum_four_characterization(n: int) -> bool:
    return n >= 8 and n % 2 == 0


def valid_witnesses(n: int, parts: tuple[int, int, int, int]) -> bool:
    return (
        sum(parts) == n
        and all(part > 0 and part % 2 == 0 for part in parts)
    )


def main() -> int:
    root = Path("/tmp/audit-work/138-audit")
    canonical = load(root / "canonical.py", "canonical_witness")
    generated = load(root / "scratch/solution.py", "generated_witness")
    cases = [
        (8, (2, 2, 2, 2)),
        (10, (4, 2, 2, 2)),
        (20, (14, 2, 2, 2)),
    ]
    for n, parts in cases:
        print(
            {
                "N": n,
                "parts": parts,
                "positive_even_sum_witness": valid_witnesses(n, parts),
                "sumFourPositiveEvens": sum_four_characterization(n),
                "canonical": canonical(n),
                "generated": generated(n),
            }
        )
    necessity_state = (2, 2, 2, 2)
    print(
        {
            "necessity_precondition_A_B_C_D": necessity_state,
            "all_positive_even": all(x > 0 and x % 2 == 0 for x in necessity_state),
            "input_sum": sum(necessity_state),
            "claimed_result": True,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
