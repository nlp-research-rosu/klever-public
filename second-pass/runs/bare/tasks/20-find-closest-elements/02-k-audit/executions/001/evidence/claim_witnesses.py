#!/usr/bin/env python3
"""Ground witnesses for every entry claim, checked against both Python bodies."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any, Callable


def load(path: pathlib.Path, name: str) -> Callable[[list[float]], Any]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


def main() -> int:
    canonical = load(pathlib.Path("/reference/canonical.py"), "claim_canonical")
    generated = load(
        pathlib.Path("/tmp/audit-work/source/solution.py"), "claim_generated"
    )
    witnesses = [
        ("claim-1", [1.0, 2.0, 3.0, 4.0, 5.0, 11.0 / 5.0], (2.0, 11.0 / 5.0), "true"),
        ("claim-2", [1.0, 2.0, 3.0, 4.0, 5.0, 2.0], (2.0, 2.0), "true"),
        ("claim-3", [1.0, 2.0], (1.0, 2.0), "A < B and not(B < A)"),
        ("claim-4", [2.0, 1.0], (1.0, 2.0), "B < A and not(A < B)"),
        ("claim-5", [2.0, 2.0], (2.0, 2.0), "A == B and neither is less"),
        ("claim-6", [-10.0, -3.0, -3.5, 9.0], (-3.5, -3.0), "true"),
    ]

    failures = 0
    for name, values, expected, precondition in witnesses:
        canonical_result = canonical(list(values))
        generated_result = generated(list(values))
        matches = canonical_result == generated_result == expected
        if not matches:
            failures += 1
        print(
            f"{name}: precondition={precondition}; input={values!r}; "
            f"claimed={expected!r}; canonical={canonical_result!r}; "
            f"generated={generated_result!r}; match={matches}"
        )
    print(f"WITNESSES={len(witnesses)}")
    print(f"FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
