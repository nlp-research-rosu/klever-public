#!/usr/bin/env python3
"""Compare fresh generated K-semantics runs with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_function(path: Path, module_name: str) -> Callable[[list[int]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    assert isinstance(module, ModuleType)
    spec.loader.exec_module(module)
    return getattr(module, "by_length")


def k_input(values: list[int]) -> str:
    sequence = " :: ".join([*(str(value) for value in values), ".PyVals"])
    return f"pyList({sequence})"


def k_expected(values: list[str]) -> str:
    rendered = " :: ".join([*(f'"{value}"' for value in values), ".PyVals"])
    return f"pyList ( {rendered} )"


def normalize(term: str) -> str:
    return re.sub(r"\s+", " ", term).strip()


canonical = load_function(Path("/reference/canonical.py"), "stage3_canonical")
generated = load_function(
    Path("/tmp/audit-work/source/solution.py"), "stage3_generated"
)

cases = [
    ("documented", [2, 1, 1, 4, 5, 8, 2, 3]),
    ("empty", []),
    ("documented_invalid", [1, -1, 55]),
    ("all_digits_ascending", list(range(1, 10))),
    ("all_digits_descending", list(range(9, 0, -1))),
    ("invalid_neighbors", [-2, -1, 0, 10, 11, 55]),
    ("duplicates_and_invalid", [9, 9, 1, 1, 5, 5, 0, 10]),
    ("large_magnitude", [-(10**100), 1, 9, 10**100]),
]

failures = 0
for index, (label, values) in enumerate(cases):
    canonical_result = canonical(values.copy())
    generated_result = generated(values.copy())
    command = [
        "krun",
        "/tmp/audit-work/source/solution.mpy",
        "--definition",
        "/tmp/audit-work/concrete-kompiled",
        f"-cINPUT={k_input(values)}",
        "--output",
        "pretty",
    ]
    print(f"CASE {index} {label}")
    print("input=" + repr(values))
    print("command=" + shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    combined = completed.stdout + completed.stderr
    log_path = Path(f"/audit-output/evidence/krun_case_{index:02d}_{label}.log")
    log_path.write_text(
        "COMMAND: "
        + shlex.join(command)
        + f"\nEXIT: {completed.returncode}\n"
        + combined,
        encoding="utf-8",
    )
    match = re.search(r"<result>(.*?)</result>", completed.stdout, re.DOTALL)
    actual_term = normalize(match.group(1)) if match else "<missing-result-cell>"
    expected_term = normalize(k_expected(canonical_result))
    print(f"exit={completed.returncode}")
    print("canonical=" + repr(canonical_result))
    print("generated=" + repr(generated_result))
    print("k_result=" + actual_term)
    print("expected_k_result=" + expected_term)
    case_ok = (
        completed.returncode == 0
        and canonical_result == generated_result
        and actual_term == expected_term
    )
    print(f"case_ok={case_ok}")
    failures += not case_ok

print(f"case_count={len(cases)}")
print(f"failure_count={failures}")
raise SystemExit(1 if failures else 0)
