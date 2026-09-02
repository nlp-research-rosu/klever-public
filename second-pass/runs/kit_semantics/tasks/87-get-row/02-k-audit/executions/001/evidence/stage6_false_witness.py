#!/usr/bin/env python3
"""Demonstrate the fresh K mutation is false for a satisfying Python input."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


def main() -> None:
    canonical = load(Path("/reference/canonical.py"), "stage6_canonical")
    generated = load(Path("/tmp/audit-work/src/solution.py"), "stage6_generated")
    matrix = [[5, 5]]
    x = 5
    raw_ref0_value = [(0, 0), (0, 1)]
    intended = [(0, 1), (0, 0)]
    assert canonical(matrix, x) == intended
    assert generated(matrix, x) == intended
    assert raw_ref0_value != intended
    print(f"input={matrix!r}, x={x}")
    print(f"mutated_ref0_value={raw_ref0_value!r}")
    print(f"canonical={canonical(matrix, x)!r}")
    print(f"generated={generated(matrix, x)!r}")
    print("mutation_is_false=true")


if __name__ == "__main__":
    main()
