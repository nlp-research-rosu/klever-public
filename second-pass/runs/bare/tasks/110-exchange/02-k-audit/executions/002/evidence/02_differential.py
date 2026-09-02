#!/usr/bin/env python3
"""Independent differential test for HumanEval/110 exchange."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import random


ROOT = Path("/tmp/audit-work/110-exchange")


def load_exchange(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


canonical = load_exchange("trusted_exchange_canonical", ROOT / "trusted/canonical.py")
generated = load_exchange("candidate_exchange_generated", ROOT / "candidate/solution.py")


def contract_oracle(lst1: list[int], lst2: list[int]) -> str:
    """Directly encode the exchange feasibility stated by the prompt."""
    odd_slots = sum(1 for value in lst1 if value % 2 == 1)
    even_donors = sum(1 for value in lst2 if value % 2 == 0)
    return "YES" if even_donors >= odd_slots else "NO"


targeted = [
    # The two documented examples.
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([1, 2, 3, 4], [1, 5, 3, 4]),
    # Empty-list boundary cases (outside the prompt's non-empty assumption).
    ([], []),
    ([], [1]),
    ([], [2]),
    ([1], []),
    ([2], []),
    # Singletons, zero, and negative parity.
    ([1], [2]),
    ([1], [3]),
    ([2], [1]),
    ([0], [-1]),
    ([-1], [-2]),
    ([-3, -2], [-4, -5]),
    # Decision boundary: below by two, below by one, exactly equal, above by one.
    ([1, 3, 2], [1, 5]),
    ([1, 3, 2], [4, 5]),
    ([1, 3, 2], [4, 6]),
    ([1, 3, 2], [4, 6, 8]),
    # Unequal lengths and repeated values.
    ([1, 1, 1, 1], [2, 2, 2, 2]),
    ([1, 1, 1, 1, 2], [2, 2, 2]),
    ([2, 2, 2, 2], [1]),
]


def check_case(lst1: list[int], lst2: list[int], label: str) -> None:
    expected = contract_oracle(lst1, lst2)
    reference = canonical(list(lst1), list(lst2))
    candidate = generated(list(lst1), list(lst2))
    if not (candidate == reference == expected):
        raise AssertionError(
            f"{label}: lst1={lst1!r} lst2={lst2!r} "
            f"oracle={expected!r} canonical={reference!r} candidate={candidate!r}"
        )


for index, (lst1, lst2) in enumerate(targeted):
    check_case(lst1, lst2, f"targeted[{index}]")
    print(
        f"TARGETED {index:02d} lst1={lst1!r} lst2={lst2!r} "
        f"result={generated(list(lst1), list(lst2))}"
    )

values = (-3, -2, -1, 0, 1, 2, 3)
nonempty_lists = [
    list(items)
    for length in (1, 2, 3)
    for items in itertools.product(values, repeat=length)
]
exhaustive_count = 0
for lst1 in nonempty_lists:
    for lst2 in nonempty_lists:
        check_case(lst1, lst2, "exhaustive")
        exhaustive_count += 1

rng = random.Random(110_2026)
random_count = 10_000
for index in range(random_count):
    len1 = rng.randint(1, 30)
    len2 = rng.randint(1, 30)
    lst1 = [rng.randint(-10**9, 10**9) for _ in range(len1)]
    lst2 = [rng.randint(-10**9, 10**9) for _ in range(len2)]
    check_case(lst1, lst2, f"random[{index}]")

print(
    "DIFFERENTIAL_OK "
    f"targeted={len(targeted)} "
    f"exhaustive={exhaustive_count} "
    f"random={random_count} "
    "mismatches=0"
)
