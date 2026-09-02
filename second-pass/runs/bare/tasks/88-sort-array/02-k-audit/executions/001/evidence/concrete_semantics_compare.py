#!/usr/bin/env python3
"""Compare fresh K concrete executions with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/88-sort-array")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


def k_list(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def normalize_k_term(text: str) -> str:
    return re.sub(r"\s+", "", text)


def extract_cell(output: str, cell: str) -> str:
    match = re.search(rf"<{cell}>(.*?)</{cell}>", output, re.DOTALL)
    if match is None:
        raise ValueError(f"missing <{cell}> cell")
    return normalize_k_term(match.group(1))


canonical = load_function("trusted_humaneval_88_concrete", SCRATCH / "trusted_canonical.py")
generated = load_function("submitted_solution_88_concrete", SCRATCH / "solution.py")

cases = [
    [],
    [0],
    [5],
    [0, 1],
    [1, 0],
    [1, 1],
    [2, 4, 3, 0, 1, 5],
    [2, 4, 3, 0, 1, 5, 6],
    [3, 3, 0, 3, 1],
    [4, 0, 3],
    [4, 0, 4],
    [10**30, 7, 0],
]

failures = []
for index, values in enumerate(cases):
    canonical_result = canonical(values.copy())
    generated_result = generated(values.copy())
    input_term = k_list(values)
    command = [
        "krun",
        "regenerated-solution.mpy",
        "--definition",
        "concrete-kompiled",
        f"-cINPUT={input_term}",
    ]
    print(f"CASE[{index}] input={values}")
    print(f"COMMAND[{index}]={shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"EXIT[{index}]={completed.returncode}")
    print(completed.stdout.rstrip())

    try:
        k_input = extract_cell(completed.stdout, "input")
        k_result = extract_cell(completed.stdout, "result")
    except ValueError as err:
        failures.append((index, str(err)))
        continue

    expected_input_term = normalize_k_term(f"ListVal({input_term})")
    expected_result_term = normalize_k_term(f"ListVal({k_list(generated_result)})")
    print(f"PY_CANONICAL[{index}]={canonical_result}")
    print(f"PY_GENERATED[{index}]={generated_result}")
    print(f"K_INPUT_NORMALIZED[{index}]={k_input}")
    print(f"K_RESULT_NORMALIZED[{index}]={k_result}")
    print(f"EXPECTED_K_RESULT[{index}]={expected_result_term}")

    if completed.returncode != 0:
        failures.append((index, f"krun exit {completed.returncode}"))
    if canonical_result != generated_result:
        failures.append((index, "Python differential mismatch"))
    if k_input != expected_input_term:
        failures.append((index, "K input cell changed"))
    if k_result != expected_result_term:
        failures.append((index, "K/Python result mismatch"))

print(f"cases={len(cases)} failures={len(failures)}")
if failures:
    print(f"FAILURES={failures}")
    raise SystemExit(1)
