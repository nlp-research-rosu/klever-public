#!/usr/bin/env python3
"""Independent differential tests for HumanEval/44."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/44-change-base")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", WORK / "canonical.py").change_base
generated = load("candidate_generated", WORK / "solution.py").change_base


def outcome(function, x: int, base: int):
    try:
        return ("return", function(x, base))
    except BaseException as error:  # Record implementation behavior, including recursion.
        return ("raise", type(error).__name__)


documented = [(8, 3, "22"), (8, 2, "1000"), (7, 2, "111")]
claim_domain_cases: list[tuple[int, int]] = []
claim_domain_cases.extend((x, base) for x, base, _ in documented)
claim_domain_cases.extend(
    [
        (0, 2),
        (0, 9),
        (1, 2),
        (1, 9),
        (2, 2),
        (8, 3),
        (9, 9),
        (10, 9),
        (31, 5),
        (999, 9),
    ]
)
for base in range(2, 10):
    for exponent in range(0, 18):
        power = base**exponent
        claim_domain_cases.extend(
            (candidate, base)
            for candidate in sorted({max(0, power - 1), power, power + 1})
        )
random_source = random.Random(440044)
claim_domain_cases.extend(
    (random_source.randrange(0, 10**50), random_source.randrange(2, 10))
    for _ in range(2000)
)
claim_domain_cases = list(dict.fromkeys(claim_domain_cases))

mismatches = []
for x, base in claim_domain_cases:
    reference_result = outcome(canonical, x, base)
    generated_result = outcome(generated, x, base)
    if reference_result != generated_result:
        mismatches.append((x, base, reference_result, generated_result))

for x, base, expected in documented:
    assert outcome(canonical, x, base) == ("return", expected)
    assert outcome(generated, x, base) == ("return", expected)

print(f"CLAIM_DOMAIN_CASES={len(claim_domain_cases)}")
print(f"CLAIM_DOMAIN_MISMATCHES={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)

outside_claim = [
    (-1, 2),
    (-5, 2),
    (-9, 9),
    (1, 0),
    (99, 10),
    (2**1200, 2),
]
print("OUTSIDE_OR_RUNTIME_BOUNDARY_PROBES:")
for x, base in outside_claim:
    print(
        f"x={x if x.bit_length() < 100 else '<2**1201>'} base={base} "
        f"canonical={outcome(canonical, x, base)!r} "
        f"generated={outcome(generated, x, base)!r}"
    )

if mismatches:
    sys.exit(1)
