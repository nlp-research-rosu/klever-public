#!/usr/bin/env python3
"""Independent differential check of canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def observe(function, args):
    try:
        value = function(*args)
        if isinstance(value, float) and math.isnan(value):
            return {"kind": "value", "type": "float", "value": "NaN"}
        return {"kind": "value", "type": type(value).__name__, "value": value}
    except Exception as error:  # Compare observable exception class and message shape.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


if len(sys.argv) != 4:
    raise SystemExit("usage: differential.py CANONICAL SOLUTION INPUTS_JSON")

canonical = load_function(Path(sys.argv[1]), "trusted_canonical")
candidate = load_function(Path(sys.argv[2]), "generated_solution")

curated = [
    ("example-valid", (3, 4, 5)),
    ("example-invalid", (1, 2, 10)),
    ("first-branch-equality", (1, 2, 3)),
    ("second-branch-equality", (1, 3, 2)),
    ("third-branch-equality", (3, 1, 2)),
    ("first-branch-invalid", (1, 1, 3)),
    ("second-branch-invalid", (1, 3, 1)),
    ("third-branch-invalid", (3, 1, 1)),
    ("first-boundary-just-valid-float", (1.0, 2.0, 2.999999)),
    ("second-boundary-just-valid-float", (1.0, 2.999999, 2.0)),
    ("third-boundary-just-valid-float", (2.999999, 1.0, 2.0)),
    ("equilateral-unit", (1, 1, 1)),
    ("isosceles-integer", (2, 2, 3)),
    ("scalene-integer", (10, 5, 7)),
    ("valid-all-floats", (5.5, 6.25, 7.75)),
    ("degenerate-all-zero", (0, 0, 0)),
    ("negative", (-1, -1, -1)),
    ("mixed-sign", (-1, 2, 2)),
    ("booleans", (True, True, True)),
    ("large-integers", (10**9, 10**9, 10**9)),
    ("missing-all-arguments", ()),
    ("missing-one-argument", (1, 2)),
    ("extra-argument", (1, 2, 2, 3)),
]

rng = random.Random(710071)
generated = []
for index in range(500):
    generated.append((f"generated-int-{index}", tuple(rng.randint(-25, 125) for _ in range(3))))
for index in range(500):
    generated.append(
        (
            f"generated-float-{index}",
            tuple(round(rng.uniform(-25.0, 125.0), 6) for _ in range(3)),
        )
    )

cases = curated + generated
Path(sys.argv[3]).write_text(
    json.dumps(
        [{"label": label, "args": list(args)} for label, args in cases],
        indent=2,
        sort_keys=True,
    )
    + "\n"
)

mismatches = []
for label, args in cases:
    left = observe(canonical, args)
    right = observe(candidate, args)
    if left != right:
        mismatches.append(
            {"label": label, "args": args, "canonical": left, "candidate": right}
        )

for label, args in curated:
    print(
        f"{label}: args={args!r} canonical={observe(canonical, args)!r} "
        f"candidate={observe(candidate, args)!r}"
    )
print(f"curated_cases={len(curated)}")
print(f"generated_integer_cases={sum(label.startswith('generated-int-') for label, _ in generated)}")
print(f"generated_float_cases={sum(label.startswith('generated-float-') for label, _ in generated)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], indent=2, default=repr))
    raise SystemExit(1)
print("DIFFERENTIAL_OK")
