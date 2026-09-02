#!/usr/bin/env python3
"""Run the freshly built generated semantics and compare results with Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shlex
import subprocess


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "semantic-clean-kompiled"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


canonical = load_entry(WORK / "reference/canonical.py", "k_audit_canonical")
candidate = load_entry(WORK / "solution.py", "k_audit_candidate")


def typed_row(row: list[int]) -> str:
    return "rowVal()" if not row else f"rowVal({','.join(map(str, row))})"


def typed_grid(grid: list[list[int]]) -> str:
    if not grid:
        return "gridVal()"
    return f"gridVal({','.join(typed_row(row) for row in grid)})"


def ordinary_row(row: list[int]) -> str:
    if not row:
        return "listVal()"
    return f"listVal({','.join(f'intVal({item})' for item in row)})"


def ordinary_grid(grid: list[list[int]]) -> str:
    if not grid:
        return "listVal()"
    return f"listVal({','.join(ordinary_row(row) for row in grid)})"


cases = [
    (
        "typed-example-1",
        [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]],
        1,
        typed_grid,
    ),
    (
        "ordinary-example-1",
        [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]],
        1,
        ordinary_grid,
    ),
    (
        "typed-example-2",
        [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]],
        2,
        typed_grid,
    ),
    (
        "ordinary-example-2",
        [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]],
        2,
        ordinary_grid,
    ),
    ("typed-empty-grid-outside-contract", [], 1, typed_grid),
    ("ordinary-empty-grid-outside-contract", [], 1, ordinary_grid),
    ("typed-empty-row-outside-contract", [[]], 1, typed_grid),
    ("ordinary-empty-row-outside-contract", [[]], 1, ordinary_grid),
    ("typed-minimum-zero", [[0]], 1, typed_grid),
    ("typed-minimum-one", [[1]], 1, typed_grid),
    ("typed-capacity-maximum", [[1]], 10, typed_grid),
    ("typed-ceil-at-boundary", [[1, 1, 1]], 3, typed_grid),
    ("typed-ceil-above-boundary", [[1, 1, 1, 1]], 3, typed_grid),
    ("typed-per-row-separation", [[1], [1]], 2, typed_grid),
    ("ordinary-per-row-separation", [[1], [1]], 2, ordinary_grid),
]

failures = 0
for name, grid, capacity, grid_encoder in cases:
    expected = canonical(grid, capacity)
    candidate_result = candidate(grid, capacity)
    args = f"{grid_encoder(grid)},intVal({capacity})"
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARGS={args}",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = completed.stdout + completed.stderr
    matches = re.findall(r"<result>\s*intVal\s*\(\s*(-?\d+)\s*\)\s*</result>", output)
    actual = int(matches[-1]) if matches else None
    print(f"CASE: {name}")
    print(f"COMMAND: {shlex.join(command)}")
    print(f"EXIT_STATUS: {completed.returncode}")
    print(f"INPUT: grid={grid!r} capacity={capacity}")
    print(
        f"RESULTS: canonical={expected} candidate_python={candidate_result} "
        f"fresh_K={actual}"
    )
    print("K_OUTPUT_BEGIN")
    print(output.rstrip())
    print("K_OUTPUT_END")
    if completed.returncode != 0 or actual != expected or candidate_result != expected:
        failures += 1

print(f"CASES={len(cases)} FAILURES={failures}")
if failures:
    raise SystemExit(1)
