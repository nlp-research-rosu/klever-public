#!/usr/bin/env python3
"""Compare fresh K execution with both independent Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys


def load_eat(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.eat


solution_mpy = Path(sys.argv[1])
definition = Path(sys.argv[2])
canonical = load_eat("canonical_for_k_compare", Path(sys.argv[3]))
generated = load_eat("generated_for_k_compare", Path(sys.argv[4]))

cases = [
    (5, 6, 10),
    (4, 8, 9),
    (1, 10, 10),
    (2, 11, 5),
    (0, 0, 0),
    (0, 0, 1000),
    (0, 1000, 0),
    (1000, 1000, 1000),
    (1000, 999, 1000),
    (1000, 1000, 999),
    (0, 500, 500),
    (0, 501, 500),
]

mismatches = 0
for case in cases:
    args_term = f"args({case[0]}, {case[1]}, {case[2]})"
    command = [
        "krun",
        str(solution_mpy),
        "--definition",
        str(definition),
        f"-cARGS={args_term}",
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    compact = re.sub(r"\s+", "", completed.stdout)
    match = re.search(r"result\((-?\d+),(-?\d+)\)", compact)
    k_value = [int(match.group(1)), int(match.group(2))] if match else None
    canonical_value = canonical(*case)
    generated_value = generated(*case)
    ok = (
        completed.returncode == 0
        and k_value == canonical_value == generated_value
    )
    mismatches += not ok
    print(
        f"case={case}; command={command!r}; exit={completed.returncode}; "
        f"K={k_value}; canonical={canonical_value}; generated={generated_value}; "
        f"match={ok}"
    )
    if completed.stderr:
        print(f"stderr={completed.stderr.strip()}")
    if match is None:
        print(f"unparsed_stdout={completed.stdout!r}")

print(f"cases={len(cases)}")
print(f"mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
