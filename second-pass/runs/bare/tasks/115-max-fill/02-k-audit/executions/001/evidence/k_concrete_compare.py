#!/usr/bin/env python3
"""Run the freshly built generated K semantics and compare with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/rebuild")
DEFINITION = WORK / "semantic-audit-kompiled"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_k_bridge")
generated = load_entry(WORK / "solution.py", "candidate_solution_k_bridge")


def typed_row(row: list[int]) -> str:
    return f"rowVal({','.join(map(str, row))})"


def typed_grid(grid: list[list[int]]) -> str:
    return f"gridVal({','.join(typed_row(row) for row in grid)})"


def ordinary_row(row: list[int]) -> str:
    return f"listVal({','.join(f'intVal({cell})' for cell in row)})"


def ordinary_grid(grid: list[list[int]]) -> str:
    return f"listVal({','.join(ordinary_row(row) for row in grid)})"


base_cases = [
    ("prompt-example-1", [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1),
    ("prompt-example-2", [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]], 2),
    ("prompt-example-3", [[0, 0, 0], [0, 0, 0]], 5),
    ("empty-grid", [], 1),
    ("empty-row", [[]], 10),
    ("min-zero", [[0]], 1),
    ("min-one", [[1]], 1),
    ("ceiling-c-minus-one", [[1, 1]], 3),
    ("ceiling-c", [[1, 1, 1]], 3),
    ("ceiling-c-plus-one", [[1, 1, 1, 1]], 3),
    ("max-width-cap-max", [[1] * 100], 10),
    ("max-height-cap-max", [[row % 2] for row in range(100)], 10),
    (
        "representative-30x30-checkerboard",
        [[(row + col) % 2 for col in range(30)] for row in range(30)],
        10,
    ),
]

tests: list[tuple[str, str, list[list[int]], int]] = []
for name, grid, capacity in base_cases:
    tests.append((name, "contract-typed", grid, capacity))

for name, grid, capacity in base_cases[:5] + base_cases[7:10]:
    tests.append((name, "ordinary-listVal", grid, capacity))

failures = 0
for name, encoding, grid, capacity in tests:
    grid_term = typed_grid(grid) if encoding == "contract-typed" else ordinary_grid(grid)
    args_term = f"{grid_term},intVal({capacity})"
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARGS={args_term}",
    ]
    print("COMMAND:", shlex.join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    match = re.search(r"<result>\s*intVal \( (-?\d+) \)\s*</result>", completed.stdout)
    k_result = int(match.group(1)) if match else None
    canonical_result = canonical(grid, capacity)
    generated_result = generated(grid, capacity)
    ok = (
        completed.returncode == 0
        and k_result == canonical_result
        and k_result == generated_result
    )
    failures += int(not ok)
    print(
        "RESULT:",
        {
            "name": name,
            "encoding": encoding,
            "krun_exit": completed.returncode,
            "k": k_result,
            "canonical_python": canonical_result,
            "generated_python": generated_result,
            "ok": ok,
        },
    )
    if not match or completed.returncode != 0:
        print("KRUN_OUTPUT_BEGIN")
        print(completed.stdout)
        print("KRUN_OUTPUT_END")

print("SUMMARY:", {"tests": len(tests), "failures": failures})
raise SystemExit(1 if failures else 0)
