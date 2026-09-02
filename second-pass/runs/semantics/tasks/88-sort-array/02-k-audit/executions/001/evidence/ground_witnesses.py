#!/usr/bin/env python3
"""Print concrete satisfying witnesses for each candidate entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scratch = Path("/tmp/audit-work/88-sort-array")
canonical = load(scratch / "canonical.py", "canonical_witness")
generated = load(scratch / "solution.py", "generated_witness")

witnesses = [
    ("empty", [], {}),
    ("singleton", [5], {"F": 5}),
    ("odd", [2, 4, 3, 0, 1, 5], {"F": 2, "MIDDLE": [4, 3, 0, 1], "L": 5}),
    (
        "even",
        [2, 4, 3, 0, 1, 5, 6],
        {"F": 2, "MIDDLE": [4, 3, 0, 1, 5], "L": 6},
    ),
]

for name, values, substitution in witnesses:
    if name == "odd":
        assert (substitution["F"] + substitution["L"]) % 2 == 1
    if name == "even":
        assert (substitution["F"] + substitution["L"]) % 2 == 0
    assert all(value >= 0 for value in values)
    canonical_result = canonical.sort_array(list(values))
    generated_result = generated.sort_array(list(values))
    assert canonical_result == generated_result
    print(
        f"{name}: input={values} substitution={substitution} "
        f"canonical={canonical_result} generated={generated_result}"
    )

print("all_four_plain_preconditions_satisfiable=yes")
print(
    "representation_note=odd/even formal heap terms contain snocVS/intsVS "
    "rather than constructor-only concrete ValSeq terms"
)
