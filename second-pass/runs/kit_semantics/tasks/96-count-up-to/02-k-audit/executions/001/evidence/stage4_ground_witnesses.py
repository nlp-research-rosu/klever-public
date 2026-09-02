#!/usr/bin/env python3
"""Ground witnesses for all positive claim preconditions and postconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def no_divisors(number: int, start: int) -> bool:
    return all(number % divisor != 0 for divisor in range(max(2, start), number))


def primes_between(start: int, stop: int) -> list[int]:
    return [
        candidate
        for candidate in range(start, stop)
        if candidate >= 2 and no_divisors(candidate, 2)
    ]


def main() -> None:
    canonical = load_module("canonical_ground_96", Path("/reference/canonical.py"))
    candidate = load_module("candidate_ground_96", Path("/candidate/solution.py"))

    inner = {
        "C": 4,
        "D": 2,
        "B": True,
        "N": 5,
        "M0": {},
        "H": 0,
        "P": [],
        "HL": 1,
        "STACK": [],
    }
    inner_pre = inner["C"] >= 2 and inner["D"] >= 2 and inner["D"] <= inner["C"]
    inner_post_pb = inner["B"] and no_divisors(inner["C"], inner["D"])

    outer = {
        "C": 2,
        "N": 5,
        "D": 2,
        "B": True,
        "M0": {},
        "H": 0,
        "P": [],
        "HL": 1,
        "STACK": [],
    }
    outer_pre = outer["C"] >= 2 and outer["C"] < outer["N"]
    outer_post_sequence = outer["P"] + primes_between(outer["C"], outer["N"])

    entry_inputs = [0, 2, 5, 20]
    entry_rows = []
    for n in entry_inputs:
        expected = primes_between(2, n)
        canonical_result = canonical.count_up_to(n)
        candidate_result = candidate.count_up_to(n)
        entry_rows.append(
            {
                "N": n,
                "precondition_N_ge_0": n >= 0,
                "claimed_primesBelow": expected,
                "canonical": canonical_result,
                "candidate": candidate_result,
                "all_equal": expected == canonical_result == candidate_result,
            }
        )

    print(
        "inner_claim_witness:",
        json.dumps(
            {
                "state": inner,
                "precondition": inner_pre,
                "claimed_final_PB": inner_post_pb,
            },
            sort_keys=True,
        ),
    )
    print(
        "outer_claim_witness:",
        json.dumps(
            {
                "state": outer,
                "precondition": outer_pre,
                "claimed_final_sequence": outer_post_sequence,
            },
            sort_keys=True,
        ),
    )
    print("entry_claim_substitutions:", json.dumps(entry_rows, sort_keys=True))

    assert inner_pre
    assert inner_post_pb is False
    assert outer_pre
    assert outer_post_sequence == [2, 3]
    assert all(row["precondition_N_ge_0"] and row["all_equal"] for row in entry_rows)


if __name__ == "__main__":
    main()
