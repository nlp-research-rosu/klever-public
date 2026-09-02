#!/usr/bin/env python3
"""Show a satisfying ground witness for each formal entry precondition."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable


def load(path: Path) -> Callable[[int, int, int], Any]:
    spec = importlib.util.spec_from_file_location(f"witness_{path.stem}_{id(path)}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def guards(a: int, b: int, c: int) -> tuple[bool, bool, bool]:
    return a + b <= c, a + c <= b, b + c <= a


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: claim_witnesses.py TRUSTED_CANONICAL SUBMITTED_SOLUTION", file=sys.stderr)
        return 64
    trusted = load(Path(sys.argv[1]))
    submitted = load(Path(sys.argv[2]))
    cases = [
        ("invalid-first", (1, 2, 3), -1),
        ("invalid-second", (2, 4, 2), -1),
        ("invalid-third", (4, 2, 2), -1),
        ("valid", (3, 4, 5), 6.0),
    ]
    rows = []
    failed = False
    for claim, values, expected in cases:
        a, b, c = values
        row = {
            "claim": claim,
            "input": values,
            "guards_in_program_order": guards(a, b, c),
            "claimed_ground_result": expected,
            "trusted_python_result": trusted(a, b, c),
            "submitted_python_result": submitted(a, b, c),
        }
        rows.append(row)
        if row["trusted_python_result"] != expected or row["submitted_python_result"] != expected:
            failed = True
    print(json.dumps(rows, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
