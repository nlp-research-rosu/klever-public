#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(path.stem + "_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


canonical = load_entry(Path("/reference/canonical.py"))
generated = load_entry(Path("/candidate/solution.py"))

named_cases = {
    "documented true": (3, 4, 5),
    "documented false": (1, 2, 3),
    "true, hypotenuse first": (5, 3, 4),
    "true, hypotenuse second": (3, 5, 4),
    "true, hypotenuse third": (3, 4, 5),
    "positive no equality": (2, 3, 4),
    "zero first boundary": (0, 3, 3),
    "zero second boundary": (3, 0, 3),
    "zero third boundary": (3, 3, 0),
    "negative first": (-3, 4, 5),
    "negative second": (3, -4, 5),
    "negative third": (3, 4, -5),
    "large true": (3000000000000, 4000000000000, 5000000000000),
    "large false": (3000000000000, 4000000000000, 5000000000001),
    "float true": (0.3, 0.4, 0.5),
    "float false": (0.3, 0.4, 0.6),
}

named_mismatches: list[tuple[str, tuple[Any, ...], Any, Any]] = []
print("NAMED CASES")
for label, args in named_cases.items():
    expected = canonical(*args)
    actual = generated(*args)
    print(f"{label}: args={args!r} canonical={expected!r} generated={actual!r}")
    if expected != actual:
        named_mismatches.append((label, args, expected, actual))

print("ARITY/EMPTY BOUNDARIES")
arity_matches = 0
for args in [(), (1,), (1, 2), (1, 2, 3, 4)]:
    outcomes = []
    for function in (canonical, generated):
        try:
            outcomes.append(("return", function(*args)))
        except Exception as error:  # deliberately compare public call behavior
            outcomes.append(("raise", type(error).__name__))
    equal = outcomes[0] == outcomes[1]
    arity_matches += equal
    print(f"args={args!r} canonical={outcomes[0]!r} generated={outcomes[1]!r} equal={equal}")

all_mismatches: list[tuple[tuple[int, int, int], bool, bool]] = []
positive_mismatches: list[tuple[tuple[int, int, int], bool, bool]] = []
for args in itertools.product(range(-20, 21), repeat=3):
    expected = canonical(*args)
    actual = generated(*args)
    if expected != actual:
        all_mismatches.append((args, expected, actual))
        if all(value > 0 for value in args):
            positive_mismatches.append((args, expected, actual))

print("GENERATED INTEGER SWEEP")
print("scope=[-20,20]^3 cases=68921")
print(f"whole_integer_mismatches={len(all_mismatches)}")
print(f"strictly_positive_mismatches={len(positive_mismatches)}")
print(f"first_20_mismatches={all_mismatches[:20]!r}")
print(f"named_mismatches={named_mismatches!r}")
print(f"arity_equal_cases={arity_matches}/4")

raise SystemExit(1 if all_mismatches or named_mismatches or arity_matches != 4 else 0)
