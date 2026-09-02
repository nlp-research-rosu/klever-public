#!/usr/bin/env python3
"""Independent differential test for HumanEval 137.

Oracle: the trusted /reference/canonical.py implementation.
Subject: the scratch copy of the candidate solution.py.

The exact input corpus and run summary are written as JSON evidence.  Built-in
integers, finite floats, numeric strings using dot/comma decimal separators,
scientific notation, signed zero, large magnitudes, invalid empty strings, and
all three result branches are represented.
"""

from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


WORK = Path("/tmp/audit-work/137-compare-one-audit")
INPUTS_OUT = Path("/audit-output/evidence/differential_inputs.json")
RESULT_OUT = Path("/audit-output/evidence/differential_result.json")


def load_function(path: Path, module_name: str) -> Callable[[Any, Any], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def encode(value: Any) -> dict[str, Any]:
    if isinstance(value, float):
        return {
            "type": "float",
            "hex": value.hex(),
            "repr": repr(value),
        }
    return {"type": type(value).__name__, "value": value}


def outcome(function: Callable[[Any, Any], Any], a: Any, b: Any) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": encode(function(a, b))}
    except Exception as error:  # Deliberately compare documented failure boundaries too.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


canonical = load_function(WORK / "trusted-canonical.py", "trusted_canonical_137")
candidate = load_function(WORK / "solution.py", "candidate_solution_137")

documented = [
    (1, 2.5),
    (1, "2,3"),
    ("5,1", "6"),
    ("1", 1),
]

boundary = [
    ("", "1"),
    ("1", ""),
    (" ", "1"),
    ("+0", -0.0),
    ("-0", "0,0"),
    (5e-324, "0"),
    (-5e-324, "-0"),
    (1.7976931348623157e308, "1e308"),
    (-1.7976931348623157e308, "-1e308"),
    (2**53 - 1, float(2**53)),
    (2**53 + 1, float(2**53)),
    ("0.10000000000000001", 0.1),
    (".5", "0,500"),
    ("1,25e2", 124.999),
    ("-1.25e-2", "-0,0124"),
    (10**400, 1),
]

atoms: list[Any] = []
atoms.extend(range(-20, 21))
atoms.extend([-(2**53 + 1), -(2**53), 2**53 - 1, 2**53, 2**53 + 1, 10**100])
atoms.extend(
    [
        -1.7976931348623157e308,
        -1e100,
        -100.5,
        -2.5,
        -1.0,
        -0.0,
        0.0,
        5e-324,
        0.1,
        0.5,
        1.0,
        1.5,
        2.5,
        100.5,
        1e100,
        1.7976931348623157e308,
    ]
)
for integer in range(-12, 13):
    atoms.extend(
        [
            str(integer),
            f"{integer}.0",
            f"{integer},0",
            f"{integer + 0.25:.2f}",
            f"{integer + 0.25:.2f}".replace(".", ","),
        ]
    )
atoms.extend(
    [
        "+0",
        "-0",
        ".5",
        "-.5",
        "1e2",
        "-1e-2",
        "1.25e2",
        "1,25e2",
        " 2.5 ",
        " 2,5 ",
    ]
)

grid = [(a, b) for a in atoms for b in atoms]

rng = random.Random(137)
generated: list[tuple[Any, Any]] = []
for _ in range(1500):
    numerator_a = rng.randint(-10**6, 10**6)
    numerator_b = rng.randint(-10**6, 10**6)
    scale_a = rng.randint(0, 6)
    scale_b = rng.randint(0, 6)
    value_a = numerator_a / (10**scale_a)
    value_b = numerator_b / (10**scale_b)

    def choose_form(value: float) -> Any:
        form = rng.randrange(4)
        if form == 0 and value.is_integer() and abs(value) < 10**12:
            return int(value)
        if form == 1:
            return float(value)
        rendered = f"{value:.6f}".rstrip("0").rstrip(".")
        if form == 3:
            rendered = rendered.replace(".", ",")
        return rendered

    generated.append((choose_form(value_a), choose_form(value_b)))

cases = documented + boundary + grid + generated
INPUTS_OUT.write_text(
    json.dumps(
        {
            "construction": (
                "documented + boundary + Cartesian product of atoms + "
                "1500 seeded generated pairs"
            ),
            "seed": 137,
            "documented": [[encode(a), encode(b)] for a, b in documented],
            "boundary": [[encode(a), encode(b)] for a, b in boundary],
            "atoms": [encode(value) for value in atoms],
            "generated": [[encode(a), encode(b)] for a, b in generated],
            "grid_is_cartesian_product_of_atoms": True,
            "total_cases": len(cases),
        },
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

mismatches: list[dict[str, Any]] = []
branch_counts = {"equal": 0, "a_larger": 0, "b_larger": 0, "exception": 0}
for index, (a, b) in enumerate(cases):
    expected = outcome(canonical, a, b)
    actual = outcome(candidate, a, b)
    if expected != actual:
        mismatches.append(
            {
                "index": index,
                "a": encode(a),
                "b": encode(b),
                "canonical": expected,
                "candidate": actual,
            }
        )
    if expected["kind"] == "exception":
        branch_counts["exception"] += 1
    else:
        value = expected["value"]
        if value["type"] == "NoneType":
            branch_counts["equal"] += 1
        elif expected == outcome(lambda _a, _b: _a, a, b):
            branch_counts["a_larger"] += 1
        else:
            branch_counts["b_larger"] += 1

summary = {
    "oracle": "/reference/canonical.py copied byte-for-byte to scratch",
    "subject": "/candidate/solution.py copied byte-for-byte to scratch",
    "total_cases": len(cases),
    "mismatch_count": len(mismatches),
    "branch_counts": branch_counts,
    "mismatches": mismatches[:100],
}
RESULT_OUT.write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
