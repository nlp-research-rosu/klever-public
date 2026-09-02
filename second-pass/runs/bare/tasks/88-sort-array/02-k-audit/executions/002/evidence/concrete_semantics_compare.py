#!/usr/bin/env python3
"""Run the rebuilt generated semantics and compare its result with CPython."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_solution(path: Path):
    spec = importlib.util.spec_from_file_location("concrete_solution", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


def render_list(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


solution = load_solution(Path("/tmp/audit-work/reconstruction/solution.py"))
cases = [
    [],
    [0],
    [5],
    [0, 1],
    [1, 1],
    [3, 1, 2, 0],
    [2, 4, 3, 0, 1, 5],
    [2, 4, 3, 0, 1, 5, 6],
    [10**30, 7, 10**30 - 1],
]
for index, case in enumerate(cases):
    input_term = render_list(case)
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "concrete-kompiled",
        f"-cINPUT={input_term}",
    ]
    result = subprocess.run(
        command,
        cwd="/tmp/audit-work/reconstruction",
        text=True,
        capture_output=True,
        check=False,
    )
    print(f"CASE {index} input={case}")
    print(f"COMMAND: {shlex.join(command)}")
    print(f"EXIT_STATUS: {result.returncode}")
    if result.stderr:
        print(f"STDERR: {result.stderr.strip()}")
    assert result.returncode == 0
    assert re.search(r"<k>\s*\.K\s*</k>", result.stdout, re.S)
    result_match = re.search(r"<result>\s*(.*?)\s*</result>", result.stdout, re.S)
    input_match = re.search(r"<input>\s*(.*?)\s*</input>", result.stdout, re.S)
    assert result_match is not None and input_match is not None
    python_result = solution(list(case))
    expected_result = f"ListVal({render_list(python_result)})"
    expected_input = f"ListVal({input_term})"
    print(f"PYTHON_RESULT: {python_result}")
    print(f"K_RESULT: {result_match.group(1).strip()}")
    assert normalize(result_match.group(1)) == normalize(expected_result)
    assert normalize(input_match.group(1)) == normalize(expected_input)
print(f"CASES={len(cases)} MISMATCHES=0 STUCK=0 INPUT_CELL_CHANGES=0")
