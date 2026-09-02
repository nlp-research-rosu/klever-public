#!/usr/bin/env python3
"""Ground witnesses for both formal claim preconditions and results."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load(Path("/tmp/audit-work/src/solution.py"), "candidate_solution")


def no_divisor_from(n: int, lo: int, hi: int) -> bool:
    return all(n % value != 0 for value in range(lo, hi + 1))


def largest_property(n: int, d: int) -> bool:
    return (
        0 < d < n
        and n % d == 0
        and no_divisor_from(n, d + 1, n - 1)
    )


n = 15
d = 14
loop_pre = (
    n > 1
    and d > 0
    and d < n
    and no_divisor_from(n, d + 1, n - 1)
)
entry_pre = n > 1
canonical_result = canonical.largest_divisor(n)
candidate_result = candidate.largest_divisor(n)

print(f"loop_witness N={n} D={d} precondition={loop_pre}")
print(f"entry_witness N={n} precondition={entry_pre}")
print(f"canonical_result={canonical_result}")
print(f"candidate_result={candidate_result}")
print(
    f"postcondition_at_candidate_result="
    f"{largest_property(n, candidate_result)}"
)

assert loop_pre and entry_pre
assert canonical_result == candidate_result == 5
assert largest_property(n, candidate_result)
