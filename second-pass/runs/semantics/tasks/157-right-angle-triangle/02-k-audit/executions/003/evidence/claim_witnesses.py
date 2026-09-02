#!/usr/bin/env python3
"""Ground witnesses for all seven formal entry-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem + "_claim_witness", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


canonical = load(Path("/reference/canonical.py"))
generated = load(Path("/candidate/solution.py"))

claims = [
    (
        "positive-hypotenuse-c",
        (3, 4, 5),
        True,
        lambda a, b, c: a > 0 and b > 0 and c > 0 and a * a + b * b == c * c,
    ),
    (
        "positive-hypotenuse-b",
        (3, 5, 4),
        True,
        lambda a, b, c: a > 0 and b > 0 and c > 0 and a * a + c * c == b * b,
    ),
    (
        "positive-hypotenuse-a",
        (5, 3, 4),
        True,
        lambda a, b, c: a > 0 and b > 0 and c > 0 and b * b + c * c == a * a,
    ),
    ("nonpositive-a", (0, 1, 2), False, lambda a, b, c: a <= 0),
    ("nonpositive-b", (1, 0, 2), False, lambda a, b, c: a > 0 and b <= 0),
    (
        "nonpositive-c",
        (1, 2, 0),
        False,
        lambda a, b, c: a > 0 and b > 0 and c <= 0,
    ),
    (
        "positive-no-equality",
        (1, 2, 3),
        False,
        lambda a, b, c: (
            a > 0
            and b > 0
            and c > 0
            and a * a + b * b != c * c
            and a * a + c * c != b * b
            and b * b + c * c != a * a
        ),
    ),
]

for name, args, claimed_result, precondition in claims:
    precondition_holds = precondition(*args)
    canonical_result = canonical(*args)
    generated_result = generated(*args)
    matches = precondition_holds and canonical_result == generated_result == claimed_result
    print(
        f"{name}: input={args} precondition={precondition_holds} "
        f"claimed={claimed_result} canonical={canonical_result} "
        f"generated={generated_result} all_match={matches}"
    )
    if not matches:
        raise SystemExit(1)

counterexample = (-3, 4, 5)
print(
    "broad_nonpositive_claim_boundary: "
    f"input={counterexample} precondition_nonpositive_a={counterexample[0] <= 0} "
    f"canonical={canonical(*counterexample)} generated={generated(*counterexample)}"
)
