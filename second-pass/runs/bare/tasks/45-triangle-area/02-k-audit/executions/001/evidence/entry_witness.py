#!/usr/bin/env python3
"""Exhibit satisfying entry states and compare claimed values to both Pythons."""

from __future__ import annotations

import fractions
import importlib.util
import pathlib


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def outcome(function, a: int, h: int):
    try:
        value = function(a, h)
        return ("value", value, fractions.Fraction.from_float(value))
    except Exception as error:
        return ("exception", type(error).__name__)


def main() -> None:
    canonical = load(pathlib.Path("/reference/canonical.py"), "canonical_witness")
    submitted = load(
        pathlib.Path("/tmp/audit-work/45-triangle-area/solution.py"),
        "submitted_witness",
    )
    cases = [
        (5, 3, "symbolic/example precondition witness"),
        (0, 99, "zero-claim precondition witness"),
        (2**53 + 1, 1, "symbolic precondition rounding witness"),
        (10**309, 1, "symbolic precondition overflow witness"),
    ]
    for a, h, label in cases:
        claimed = fractions.Fraction(a * h, 2)
        print(f"case={label}")
        print(
            "  entry_state="
            f"<k>triangleProgram</k> <args>Args({a},{h})</args> "
            "<env>.Map</env> <result>noResult</result>"
        )
        print(f"  formal_claimed_exact={claimed!r}")
        print(f"  canonical={outcome(canonical, a, h)!r}")
        print(f"  submitted={outcome(submitted, a, h)!r}")


if __name__ == "__main__":
    main()
