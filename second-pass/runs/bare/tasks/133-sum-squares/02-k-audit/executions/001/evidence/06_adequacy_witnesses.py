#!/usr/bin/env python3
"""Concrete satisfying inputs for every entry/helper claim."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
from typing import Callable


SCRATCH = Path("/tmp/audit-work/133-sum-squares")


def load_entry(path: Path, module_name: str) -> Callable[[list[object]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_entry(SCRATCH / "trusted/canonical.py", "witness_canonical")
candidate = load_entry(SCRATCH / "solution.py", "witness_candidate")

witnesses = [
    ("ground-14", [1, 2, 3], 14),
    ("universal-empty", [], 0),
    (
        "universal-rational",
        [Fraction(14, 10), Fraction(-24, 10)],
        8,
    ),
    ("ground-29", [Fraction(14, 10), Fraction(42, 10), 0], 29),
    ("ground-6", [Fraction(-24, 10), 1, 1], 6),
]

print("ENTRY_CLAIM_WITNESSES")
failures = 0
for claim, values, formal_result in witnesses:
    oracle = canonical(values)
    actual = candidate(values)
    print(
        f"claim={claim} input={values!r} formal={formal_result} "
        f"canonical={oracle} candidate={actual}"
    )
    failures += int(formal_result != oracle or formal_result != actual)

values = [Fraction(14, 10), Fraction(-24, 10)]
accumulator = 5
formal_loop_result = 13
oracle_adjusted = accumulator + canonical(values)
candidate_adjusted = accumulator + candidate(values)
print("LOOP_CLAIM_WITNESS")
print(
    "state=<functions>.Map</functions>, "
    "<env>binding(\"total\",intVal(5)).Env</env>, "
    "L=cons(ratVal(14,ten),cons(ratVal(-24,ten),nil))"
)
print(
    f"A={accumulator} input={values!r} formal={formal_loop_result} "
    f"A+canonical={oracle_adjusted} A+candidate={candidate_adjusted}"
)
failures += int(
    formal_loop_result != oracle_adjusted
    or formal_loop_result != candidate_adjusted
)

print(f"SUMMARY: witnesses=6 failures={failures}")
raise SystemExit(1 if failures else 0)
