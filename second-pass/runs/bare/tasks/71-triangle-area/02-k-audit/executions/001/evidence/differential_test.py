#!/usr/bin/env python3
"""Independent canonical-versus-submitted differential test.

The explicit corpus contains the documented examples, an empty argument list,
zero/degenerate sides, each ordered guard boundary, nearby valid triangles,
float inputs, and a large-integer Python overflow boundary.  The generated
corpus exhausts small integer triples and uses a fixed seed for broader integer
and finite-float samples.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Any, Callable


def load(path: Path, name: str) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


canonical = load(Path("/reference/canonical.py"), "trusted_canonical")
submitted = load(
    Path("/tmp/audit-work/71-triangle-area/solution.py"), "submitted_solution"
)


def outcome(fn: Callable[..., Any], args: tuple[Any, ...]) -> tuple[str, Any]:
    try:
        return ("return", fn(*args))
    except Exception as err:  # Differentially compare exception class and text.
        return ("raise", (type(err).__name__, str(err)))


def same(left: tuple[str, Any], right: tuple[str, Any]) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "raise":
        return left[1] == right[1]
    lv, rv = left[1], right[1]
    if isinstance(lv, float) and isinstance(rv, float):
        if math.isnan(lv) and math.isnan(rv):
            return True
    return type(lv) is type(rv) and lv == rv


explicit: list[tuple[str, tuple[Any, ...]]] = [
    ("empty-arity", ()),
    ("example-valid", (3, 4, 5)),
    ("example-invalid", (1, 2, 10)),
    ("all-zero", (0, 0, 0)),
    ("first-guard-equality", (1, 2, 3)),
    ("first-guard-valid-side", (2, 2, 3)),
    ("second-guard-equality", (1, 3, 2)),
    ("second-guard-valid-side", (2, 3, 2)),
    ("third-guard-equality", (3, 2, 1)),
    ("third-guard-valid-side", (3, 2, 2)),
    ("negative-length", (-1, 2, 2)),
    ("equilateral-rounding", (2, 2, 2)),
    ("exact-heron", (5, 12, 13)),
    ("float-valid", (0.5, 0.5, 0.75)),
    ("float-boundary", (0.5, 0.5, 1.0)),
    ("float-near-boundary", (0.5, 0.5, math.nextafter(1.0, 0.0))),
    ("large-finite", (10**100, 10**100, 10**100)),
    ("integer-to-float-overflow", (10**400, 10**400, 10**400)),
]

rng = random.Random(710071)
generated: list[tuple[Any, ...]] = []
generated.extend(
    (a, b, c)
    for a in range(-2, 9)
    for b in range(-2, 9)
    for c in range(-2, 9)
)
generated.extend(
    tuple(rng.randint(-10_000, 10_000) for _ in range(3)) for _ in range(250)
)
generated.extend(
    tuple(round(rng.uniform(-100.0, 100.0), 6) for _ in range(3))
    for _ in range(250)
)

mismatches: list[tuple[str, tuple[Any, ...], Any, Any]] = []
print("EXPLICIT CASES")
for label, args in explicit:
    expected = outcome(canonical, args)
    actual = outcome(submitted, args)
    print(f"{label}: args={args!r} canonical={expected!r} submitted={actual!r}")
    if not same(expected, actual):
        mismatches.append((label, args, expected, actual))

for index, args in enumerate(generated):
    expected = outcome(canonical, args)
    actual = outcome(submitted, args)
    if not same(expected, actual):
        mismatches.append((f"generated-{index}", args, expected, actual))

print("GENERATED CORPUS")
print("small_integer_triples=1331 range_each=[-2,8]")
print("seed=710071 random_integer_triples=250 range_each=[-10000,10000]")
print("seed=710071 random_float_triples=250 range_each=[-100.0,100.0]")
print(f"total_calls={len(explicit) + len(generated)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
