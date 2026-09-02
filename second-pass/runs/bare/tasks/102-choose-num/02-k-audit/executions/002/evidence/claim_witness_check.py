#!/usr/bin/env python3
"""Ground witnesses for each of the four exact and four contract claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


def no_even_in_range(x: int, y: int) -> bool:
    return x > y or (x == y and x % 2 != 0)


def choose_num_contract(x: int, y: int, result: int) -> bool:
    return (
        result == -1 and no_even_in_range(x, y)
    ) or (
        result != -1
        and x <= result <= y
        and result % 2 == 0
        and y < result + 2
    )


def main() -> int:
    canonical = load_function(
        "witness_canonical", Path("/tmp/audit-work/reference/canonical.py")
    )
    candidate = load_function(
        "witness_candidate", Path("/tmp/audit-work/candidate-src/solution.py")
    )
    witnesses = [
        ("empty", 13, 12, -1, lambda x, y: x > y),
        ("even_upper", 1, 2, 2, lambda x, y: x <= y and y % 2 == 0),
        (
            "odd_upper_with_room",
            2,
            3,
            2,
            lambda x, y: x < y and y % 2 != 0,
        ),
        (
            "odd_singleton",
            3,
            3,
            -1,
            lambda x, y: x == y and y % 2 != 0,
        ),
    ]
    for name, x, y, claimed, branch_precondition in witnesses:
        assert x > 0 and y > 0 and branch_precondition(x, y)
        reference_value = canonical(x, y)
        candidate_value = candidate(x, y)
        contract_value = choose_num_contract(x, y, claimed)
        print(
            f"{name}: x={x} y={y} claimed={claimed} "
            f"canonical={reference_value} candidate={candidate_value} "
            f"contract={contract_value}"
        )
        assert claimed == reference_value == candidate_value
        assert contract_value
    print("CLAIM_WITNESSES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
