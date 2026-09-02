#!/usr/bin/env python3
"""Execute the fresh generated K semantics and compare with both Python bodies."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import re
import shlex
import subprocess
from typing import Callable


SCRATCH = Path("/tmp/audit-work/133-sum-squares")
K_CELL = re.compile(
    r"<k>\s*intVal\s*\(\s*(-?\d+)\s*\)\s*~>\s*\.K\s*</k>", re.DOTALL
)


def load_entry(path: Path, module_name: str) -> Callable[[list[object]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_entry(SCRATCH / "trusted/canonical.py", "concrete_canonical")
candidate = load_entry(SCRATCH / "solution.py", "concrete_candidate")

cases: list[tuple[str, list[object], str]] = [
    ("empty", [], "listVal(nil)"),
    (
        "example-14",
        [1, 2, 3],
        "listVal(cons(intVal(1), cons(intVal(2), cons(intVal(3), nil))))",
    ),
    (
        "example-98",
        [1, 4, 9],
        "listVal(cons(intVal(1), cons(intVal(4), cons(intVal(9), nil))))",
    ),
    (
        "example-84",
        [1, 3, 5, 7],
        "listVal(cons(intVal(1), cons(intVal(3), "
        "cons(intVal(5), cons(intVal(7), nil)))))",
    ),
    (
        "example-29",
        [Fraction(14, 10), Fraction(42, 10), 0],
        "listVal(cons(ratVal(14, ten), "
        "cons(ratVal(42, ten), cons(intVal(0), nil))))",
    ),
    (
        "example-6",
        [Fraction(-24, 10), 1, 1],
        "listVal(cons(ratVal(-24, ten), "
        "cons(intVal(1), cons(intVal(1), nil))))",
    ),
    ("zero", [0], "listVal(cons(intVal(0), nil))"),
    ("positive-integer", [1], "listVal(cons(intVal(1), nil))"),
    ("negative-integer", [-1], "listVal(cons(intVal(-1), nil))"),
    ("just-above-zero", [Fraction(1, 10)], "listVal(cons(ratVal(1, ten), nil))"),
    ("just-below-zero", [Fraction(-1, 10)], "listVal(cons(ratVal(-1, ten), nil))"),
    ("below-one", [Fraction(9, 10)], "listVal(cons(ratVal(9, ten), nil))"),
    ("at-one", [Fraction(10, 10)], "listVal(cons(ratVal(10, ten), nil))"),
    ("above-one", [Fraction(11, 10)], "listVal(cons(ratVal(11, ten), nil))"),
    ("above-minus-one", [Fraction(-9, 10)], "listVal(cons(ratVal(-9, ten), nil))"),
    ("at-minus-one", [Fraction(-10, 10)], "listVal(cons(ratVal(-10, ten), nil))"),
    ("below-minus-one", [Fraction(-11, 10)], "listVal(cons(ratVal(-11, ten), nil))"),
    (
        "non-ten-denominator",
        [Fraction(4, 3), Fraction(-4, 3)],
        "listVal(cons(ratVal(4, next(next(one))), "
        "cons(ratVal(-4, next(next(one))), nil)))",
    ),
    (
        "large-integers",
        [10**20, -(10**20)],
        "listVal(cons(intVal(100000000000000000000), "
        "cons(intVal(-100000000000000000000), nil)))",
    ),
]

mismatches = 0
for label, python_input, k_input in cases:
    command = [
        "krun",
        str(SCRATCH / "solution.mpy"),
        "--definition",
        str(SCRATCH / "audit-semantic-kompiled"),
        f"-cARGS={k_input}",
    ]
    print(f"\nCASE: {label}")
    print("COMMAND: " + shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"EXIT_STATUS: {completed.returncode}")
    if completed.stderr:
        print("STDERR:")
        print(completed.stderr[:4000])
    match = K_CELL.search(completed.stdout)
    k_result = int(match.group(1)) if match else None
    oracle_result = canonical(python_input)
    candidate_result = candidate(python_input)
    print(
        f"INPUT: python={python_input!r} k={k_input}\n"
        f"RESULT: canonical={oracle_result!r} "
        f"candidate={candidate_result!r} k={k_result!r}"
    )
    if (
        completed.returncode != 0
        or k_result != oracle_result
        or candidate_result != oracle_result
    ):
        mismatches += 1
        print("RELEVANT_STDOUT:")
        print(completed.stdout[:6000])

print(f"\nSUMMARY: cases={len(cases)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
