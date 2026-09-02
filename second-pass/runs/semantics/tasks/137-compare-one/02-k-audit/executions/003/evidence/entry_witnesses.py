#!/usr/bin/env python3
"""One satisfying ground witness for each of the nine entry-claim sort pairs."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def observed(function, a: Any, b: Any) -> tuple[str, str]:
    try:
        value = function(a, b)
        return (type(value).__name__, repr(value))
    except Exception as error:  # noqa: BLE001
        return (type(error).__name__, str(error))


def main() -> None:
    canonical = load(Path("/reference/canonical.py"), "witness_canonical")
    submitted = load(
        Path("/tmp/audit-work/137-compare-one/solution.py"), "witness_submitted"
    )
    witnesses = [
        ("int-int", 1, 2),
        ("int-float", 1, 2.5),
        ("int-str", 1, "2,3"),
        ("float-int", 2.5, 1),
        ("float-float", 1.0, 1.0),
        ("float-str", 3.0, "3,0"),
        ("str-int", "1", 1),
        ("str-float", "2,5", 2.0),
        ("str-str", "5,1", "6"),
    ]
    for label, a, b in witnesses:
        canonical_result = observed(canonical, a, b)
        submitted_result = observed(submitted, a, b)
        print(
            f"{label}: a={a!r} b={b!r} "
            f"canonical={canonical_result!r} submitted={submitted_result!r}"
        )
        if canonical_result != submitted_result:
            raise AssertionError(f"witness disagreement for {label}")


if __name__ == "__main__":
    main()
