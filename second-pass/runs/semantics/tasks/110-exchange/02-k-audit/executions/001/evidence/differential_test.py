#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py against solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


def load_exchange(path: Path, module_name: str) -> Callable[[list, list], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


canonical = load_exchange(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_exchange(
    Path("/tmp/audit-work/exchange-110-fresh/solution.py"), "generated_solution"
)


documented = [
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([1, 2, 3, 4], [1, 5, 3, 4]),
]

boundaries = [
    ([], []),  # explicitly outside the stated non-empty domain
    ([], [1]),
    ([1], []),
    ([2], [1]),  # zero odd versus zero even
    ([1], [2]),  # equality boundary: one odd, one even
    ([1, 3], [2]),  # just over boundary: two odd, one even
    ([1], [2, 4]),  # just under boundary
    ([-3, -2], [-4, 5]),  # negative odd/even modulo behavior
    ([-5], [-3]),  # negative odd and no even donor
    ([0], [0]),  # zero is even
    ([10**100 + 1], [-(10**100)]),  # unbounded Python integers
    ([10**100 + 1, -7], [-(10**100), 2]),
]


def compare(cases: list[tuple[list[Any], list[Any]]]) -> list[dict[str, Any]]:
    mismatches = []
    for left, right in cases:
        expected = canonical(list(left), list(right))
        actual = generated(list(left), list(right))
        if expected != actual:
            mismatches.append(
                {
                    "lst1": left,
                    "lst2": right,
                    "canonical": expected,
                    "generated": actual,
                }
            )
    return mismatches


values = (-3, -2, -1, 0, 1, 2, 3)
small_lists = [
    list(items)
    for length in (1, 2, 3)
    for items in itertools.product(values, repeat=length)
]
exhaustive_integer_cases = [
    (left, right) for left in small_lists for right in small_lists
]

rng = random.Random(110)
generated_integer_cases = [
    (
        [rng.randint(-(10**9), 10**9) for _ in range(rng.randint(1, 8))],
        [rng.randint(-(10**9), 10**9) for _ in range(rng.randint(1, 8))],
    )
    for _ in range(5000)
]

# The prompt says "numbers", while the K claim is explicitly restricted to
# integers. These cases document the behavior beyond the formal K domain.
exploratory_noninteger_cases = [
    ([0.5], [1.0]),
    ([1.5], [3.0]),
    ([-0.5], [5.0]),
    ([3.0], [2.0]),
    ([2.0], [1.0]),
]

groups = [
    ("documented", documented, True),
    ("boundary_including_empty", boundaries, True),
    ("exhaustive_nonempty_integer_len_1_to_3", exhaustive_integer_cases, True),
    ("seeded_nonempty_integer", generated_integer_cases, True),
    ("exploratory_noninteger", exploratory_noninteger_cases, False),
]

required_mismatch_count = 0
for name, cases, in_required_integer_scope in groups:
    mismatches = compare(cases)
    print(
        f"{name}: cases={len(cases)} mismatches={len(mismatches)} "
        f"required_integer_scope={in_required_integer_scope}"
    )
    for mismatch in mismatches[:10]:
        print(f"  mismatch={mismatch!r}")
    if in_required_integer_scope:
        required_mismatch_count += len(mismatches)

print(f"required_integer_scope_total_mismatches={required_mismatch_count}")
raise SystemExit(1 if required_mismatch_count else 0)
