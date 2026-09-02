#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


DEFINITION = Path("/tmp/audit-work/build/semantic-llvm-kompiled")
PROGRAM = Path("/tmp/audit-work/candidate-src/solution.mpy")


@dataclass(frozen=True)
class Case:
    name: str
    k_args: str
    numbers: list[float]
    threshold: float


def load(path: Path, name: str) -> Callable[[list[float], float], bool]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "concrete_canonical")
    generated = load(
        Path("/tmp/audit-work/candidate-src/solution.py"), "concrete_generated"
    )
    cases = [
        Case(
            "prompt_false",
            "VList(VRat(10,10),VRat(20,10),VRat(30,10)),VRat(5,10)",
            [1.0, 2.0, 3.0],
            0.5,
        ),
        Case(
            "prompt_true",
            "VList(VRat(10,10),VRat(28,10),VRat(30,10),"
            "VRat(40,10),VRat(50,10),VRat(20,10)),VRat(3,10)",
            [1.0, 2.8, 3.0, 4.0, 5.0, 2.0],
            0.3,
        ),
        Case("empty", "VList(),VRat(1,1)", [], 1.0),
        Case("singleton", "VList(VRat(1,1)),VRat(1,1)", [1.0], 1.0),
        Case("claim03_empty_int", "VList(),VInt(0)", [], 0.0),
        Case("claim04_singleton_int", "VList(VInt(7)),VInt(-3)", [7.0], -3.0),
        Case("claim05_pair_int", "VList(VInt(0),VInt(1)),VInt(2)", [0.0, 1.0], 2.0),
        Case(
            "claim06_triple_int",
            "VList(VInt(0),VInt(5),VInt(5)),VInt(1)",
            [0.0, 5.0, 5.0],
            1.0,
        ),
        Case(
            "claim07_quad_int",
            "VList(VInt(0),VInt(10),VInt(20),VInt(20)),VInt(1)",
            [0.0, 10.0, 20.0, 20.0],
            1.0,
        ),
        Case(
            "strict_equal",
            "VList(VRat(10,10),VRat(15,10)),VRat(5,10)",
            [1.0, 1.5],
            0.5,
        ),
        Case(
            "strict_just_above",
            "VList(VRat(10,10),VRat(15,10)),VRat(5000001,10000000)",
            [1.0, 1.5],
            0.5000001,
        ),
        Case(
            "later_pair",
            "VList(VRat(0,1),VRat(100,10),VRat(101,10)),VRat(2,10)",
            [0.0, 10.0, 10.1],
            0.2,
        ),
        Case(
            "negative_threshold",
            "VList(VRat(1,1),VRat(1,1)),VRat(-1,1)",
            [1.0, 1.0],
            -1.0,
        ),
        # Natural exact-decimal VRat encoding disagrees with CPython binary
        # float arithmetic here:
        # exact decimal gap = 4e-17 < 5e-17, binary-float gap ~= 5.55e-17.
        Case(
            "float_rounding_witness",
            "VList(VRat(30000000000000004,100000000000000000),"
            "VRat(3,10)),VRat(5,100000000000000000)",
            [0.30000000000000004, 0.3],
            5e-17,
        ),
    ]

    mismatches = 0
    for case in cases:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cARGS={case.k_args}",
        ]
        result = subprocess.run(command, text=True, capture_output=True)
        combined = result.stdout + result.stderr
        match = re.search(r"VBool\s*\(\s*(true|false)\s*\)", combined)
        k_value = None if match is None else match.group(1) == "true"
        canonical_value = canonical(list(case.numbers), case.threshold)
        generated_value = generated(list(case.numbers), case.threshold)
        agrees = (
            result.returncode == 0
            and k_value is not None
            and k_value == canonical_value
            and k_value == generated_value
        )
        if not agrees:
            mismatches += 1
        print(f"CASE {case.name}")
        print("COMMAND: " + shlex.join(command))
        print(f"EXIT_STATUS: {result.returncode}")
        print("K_OUTPUT: " + " ".join(combined.split()))
        print(
            f"VALUES: k={k_value!r} canonical={canonical_value!r} "
            f"generated={generated_value!r} all_agree={agrees}"
        )
    print(f"TOTAL_CASES: {len(cases)}")
    print(f"MISMATCHES: {mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
