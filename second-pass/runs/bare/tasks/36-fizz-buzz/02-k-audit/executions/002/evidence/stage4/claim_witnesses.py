#!/usr/bin/env python3
"""Ground witnesses for every entry precondition and result substitution."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/36-fizz-buzz-audit-002")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


candidate = load_function(
    "candidate_solution_witness", SCRATCH / "candidate" / "solution.py"
)
canonical = load_function(
    "trusted_canonical_witness", SCRATCH / "trusted" / "canonical.py"
)


def decimal_sevens(value: int) -> int:
    assert value >= 0
    return str(value).count("7")


def suffix_result(start: int, end: int) -> int:
    assert 0 <= start <= end
    return sum(
        decimal_sevens(value)
        for value in range(start, end)
        if value % 11 == 0 or value % 13 == 0
    )


inner_x = 77
inner_count = 5
print(
    "INNER witness: X=77 C=5 i=77 n=79 x=77; "
    f"X>=0 is true; destination count={inner_count + decimal_sevens(inner_x)} "
    "x=0"
)

outer_i = 77
outer_n = 79
outer_count = 5
outer_add = suffix_result(outer_i, outer_n)
print(
    "OUTER witness: I=77 N=79 C=5 x=0; "
    f"0<=I<=N is true; destination count={outer_count + outer_add} "
    f"i={outer_n} x=0"
)

for value in [-3, 0, 79, 178, 777]:
    mathematical = (
        suffix_result(0, value) if value >= 0 else 0
    )
    candidate_result = candidate(value)
    canonical_result = canonical(value)
    print(
        f"ENTRY witness N={value}: claimed_result={mathematical} "
        f"candidate_python={candidate_result} canonical_python={canonical_result}"
    )
    assert mathematical == candidate_result == canonical_result
