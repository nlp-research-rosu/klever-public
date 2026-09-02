#!/usr/bin/env python3
"""Concrete satisfying witnesses for every candidate entry-claim precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_witness", "/reference/canonical.py")
generated = load(
    "generated_witness",
    "/tmp/audit-work/77-iscube.RDpOYi/reconstruction/solution.py",
)

witnesses = [
    ("implementation", {"A": 8}, 8, True),
    ("positive-cubes-small", {"N": 2}, 2**3, True),
    ("negative-cubes-small", {"N": 2}, -(2**3), True),
    ("positive-noncubes", {"N": 2, "D": 1}, 2**3 + 1, False),
    ("negative-noncubes", {"N": 2, "D": 1}, -(2**3 + 1), False),
    (
        "positive-cubes-false-conclusion",
        {"N": 10**15},
        (10**15) ** 3,
        True,
    ),
    (
        "negative-cubes-false-conclusion",
        {"N": 10**15},
        -((10**15) ** 3),
        True,
    ),
]

for claim, substitution, value, claimed in witnesses:
    print(
        {
            "claim": claim,
            "substitution": substitution,
            "input": value,
            "claimed_result": claimed,
            "canonical_result": canonical.iscube(value),
            "generated_result": generated.iscube(value),
        }
    )

large_root = 10**15
large_cube = large_root**3
floating_root = large_cube ** (1 / 3)
rounded_root = int(round(floating_root))
print(
    {
        "false_rule_witness_N": large_root,
        "N_cubed": large_cube,
        "python_float_cube_root": floating_root,
        "python_rounded_cube_root": rounded_root,
        "rounded_root_delta": rounded_root - large_root,
        "rounded_root_cubed_equals_input": rounded_root**3 == large_cube,
    }
)
