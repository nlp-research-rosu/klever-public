#!/usr/bin/env python3
"""Ground witnesses for the loop and end-to-end claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_count


canonical = load_entry("canonical_witness", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_witness",
    Path("/tmp/audit-work/155-even-odd-count-audit/source/solution.py"),
)


def formal_even_odd(nonnegative: int, even: int = 0, odd: int = 0):
    assert nonnegative >= 0
    while nonnegative > 0:
        if nonnegative % 2 == 0:
            even += 1
        else:
            odd += 1
        nonnegative //= 10
    return even, odd


loop_n, loop_e, loop_o = 12, 0, 0
loop_result = formal_even_odd(loop_n, loop_e, loop_o)
print(
    "loop_witness="
    f"N={loop_n},E={loop_e},O={loop_o},INPUT=99,"
    f"precondition={loop_n >= 0},formal_result={loop_result},"
    f"candidate_python={candidate(loop_n)},canonical_python={canonical(loop_n)}"
)

for value in [12, 0]:
    formal_result = formal_even_odd(abs(value))
    print(
        "entry_witness="
        f"N={value},precondition=True,formal_expected={formal_result},"
        f"candidate_python={candidate(value)},canonical_python={canonical(value)}"
    )
