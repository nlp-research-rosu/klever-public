#!/usr/bin/env python3
"""Ground substitutions into SPEC's mathematical result expression."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.monotonic


def claimed_result(values: list[int]) -> bool:
    ascending = sorted(values)
    return values == ascending or values == list(reversed(ascending))


def main() -> None:
    canonical = load(Path("/reference/canonical.py"), "canonical_for_substitution")
    candidate = load(Path("/candidate/solution.py"), "candidate_for_substitution")
    witnesses = [
        [],
        [1, 2, 4, 20],
        [4, 1, 0, -10],
        [1, 20, 4, 10],
        [3, 3, 3],
    ]
    for values in witnesses:
        formal = claimed_result(values)
        trusted_python = canonical(values.copy())
        generated_python = candidate(values.copy())
        print(
            repr(values),
            "formal=", formal,
            "canonical=", trusted_python,
            "candidate=", generated_python,
        )
        if not (formal == trusted_python == generated_python):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
