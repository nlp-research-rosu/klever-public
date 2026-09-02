#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare with both Python entries."""

from __future__ import annotations

import importlib.util
import math
import pathlib
import re
import struct
import subprocess
import sys
from fractions import Fraction


BUILD = pathlib.Path("/tmp/audit-work/build")
DEFINITION = BUILD / "semantic-kompiled"
PROGRAM = BUILD / "solution.mpy"


def load_entry(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.truncate_number


def float_bits(value: float) -> int:
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def canonical_parts(value: float) -> tuple[int, int, int]:
    exact = Fraction.from_float(value)
    integer = exact.numerator // exact.denominator
    fraction = exact - integer
    return integer, fraction.numerator, fraction.denominator


def parse_result(stdout: str) -> Fraction:
    result_cell = re.search(r"<result>(.*?)</result>", stdout, re.DOTALL)
    if result_cell is None:
        raise ValueError("no <result> cell")
    match = re.search(
        r"num\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\)",
        result_cell.group(1),
    )
    if match is None:
        raise ValueError(f"non-num result: {result_cell.group(1)!r}")
    integer, numerator, scale = map(int, match.groups())
    return Fraction(integer) + Fraction(numerator, scale)


def main() -> int:
    canonical = load_entry(pathlib.Path("/reference/canonical.py"), "canonical_for_k")
    generated = load_entry(BUILD / "solution.py", "generated_for_k")
    cases = [
        ("prompt-example", 3.5),
        ("smallest-subnormal", float.fromhex("0x0.0000000000001p-1022")),
        ("below-one", math.nextafter(1.0, 0.0)),
        ("one", 1.0),
        ("above-one", math.nextafter(1.0, math.inf)),
        ("below-2**52", math.nextafter(float(2**52), 0.0)),
        ("2**52", float(2**52)),
        ("representative-fraction", 110842303990605.02),
        ("max-finite", sys.float_info.max),
    ]
    failures = 0

    print(f"fresh_definition={DEFINITION}")
    print(f"program={PROGRAM}")
    print(f"cases={len(cases)}")
    for label, value in cases:
        integer, numerator, scale = canonical_parts(value)
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cIPART={integer}",
            f"-cFRAC={numerator}",
            f"-cSCALE={scale}",
        ]
        print("COMMAND:", " ".join(command))
        run = subprocess.run(
            command,
            cwd=BUILD,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(run.stdout, end="")
        print(f"KRUN_EXIT={run.returncode}")

        expected = canonical(value)
        actual = generated(value)
        python_same = (
            isinstance(expected, float)
            and isinstance(actual, float)
            and float_bits(expected) == float_bits(actual)
        )
        try:
            k_fraction = parse_result(run.stdout)
            k_same = k_fraction == Fraction.from_float(expected)
        except Exception as error:
            k_fraction = f"{type(error).__name__}: {error}"
            k_same = False

        ok = run.returncode == 0 and python_same and k_same
        if not ok:
            failures += 1
        print(
            f"COMPARE label={label} input={value!r} "
            f"parts=({integer},{numerator},{scale}) canonical={expected!r} "
            f"generated={actual!r} k_exact={k_fraction!s} "
            f"python_same_bits={python_same} k_same_exact={k_same} ok={ok}"
        )

    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
