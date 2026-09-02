#!/usr/bin/env python3
"""Concrete satisfying entry-precondition witnesses and their real results."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


def positive_ints(values):
    return all(isinstance(value, int) and value > 0 for value in values)


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "canonical_witness")
    generated = load(
        Path("/tmp/audit-work/candidate-src/solution.py"), "generated_witness"
    )
    witnesses = [[], [1], [2], [15, 33, 1422, 1]]
    rows = []
    for values in witnesses:
        rows.append(
            {
                "input": values,
                "positiveInts": positive_ints(values),
                "canonical": canonical(list(values)),
                "generated": generated(list(values)),
            }
        )
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
