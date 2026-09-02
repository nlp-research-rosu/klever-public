#!/usr/bin/env python3
"""Independent CPython outputs corresponding to the recorded K concrete cases."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


def main() -> None:
    candidate = load(
        Path("/tmp/audit-work/candidate-src/solution.py"), "concrete_candidate"
    )
    canonical = load(
        Path("/tmp/audit-work/reference/canonical.py"), "concrete_canonical"
    )
    cases = {
        "prompt_one": ["a", 3.14, 5],
        "empty": [],
        "bool_boundary": [True, False, 0, -4, 2.0],
        "constructors": ["x", 2.0, 7, True, [9], {}, None, object(), -1],
        "large_duplicate": [10**80, "skip", 10**80, -(10**80)],
    }
    for name, values in cases.items():
        expected = canonical(values)
        actual = candidate(values)
        print(f"PYTHON_CASE {name} expected={expected!r} actual={actual!r}")
        if actual != expected:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
