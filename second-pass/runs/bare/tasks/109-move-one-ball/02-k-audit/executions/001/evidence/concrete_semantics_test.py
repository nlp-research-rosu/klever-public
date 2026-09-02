#!/usr/bin/env python3
"""Compare rebuilt generated K semantics with Python and a generic-loop variant."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
from typing import Callable


SOURCE = Path("/tmp/audit-work/source")
ORIGINAL_DEF = Path("/tmp/audit-work/build/semantic-llvm-kompiled")
GENERIC_DEF = Path("/tmp/audit-work/build/semantic-generic-llvm-kompiled")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], object]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


def ilist(values: list[int]) -> str:
    if not values:
        return ".IList"
    return " :: ".join(map(str, values)) + " :: .IList"


def run_krun(program: Path, definition: Path, values: list[int]) -> tuple[str, object]:
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cINPUT={ilist(values)}",
    ]
    print("$", " ".join(command))
    result = subprocess.run(command, text=True, capture_output=True)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    print(f"EXIT_STATUS: {result.returncode}")
    if result.returncode != 0:
        raise RuntimeError(f"krun failed: {command}")
    boolean = re.search(
        r"<k>\s*bVal\s*\(\s*(true|false)\s*\)\s*~>\s*\.K\s*</k>",
        result.stdout,
        re.DOTALL,
    )
    if boolean:
        return result.stdout, boolean.group(1) == "true"
    integer = re.search(
        r"<k>\s*iVal\s*\(\s*(-?[0-9]+)\s*\)\s*~>\s*\.K\s*</k>",
        result.stdout,
        re.DOTALL,
    )
    if integer:
        return result.stdout, int(integer.group(1))
    raise RuntimeError(f"no bVal/iVal result in output: {result.stdout}")


original_python = load_entry(SOURCE / "solution.py", "original_python")
observe_python = load_entry(
    Path("/audit-output/evidence/observe_continuation.py"), "observe_python"
)
body_python = load_entry(Path("/audit-output/evidence/body_mutation.py"), "body_python")

programs = [
    (
        "original",
        SOURCE / "solution.mpy",
        original_python,
        [
            [],
            [0],
            [2, 1],
            [1, 2],
            [3, 4, 5, 1, 2],
            [3, 5, 4, 1, 2],
            [2, 1, 3],
            [-1, -3, -2],
            [10**30, -(10**30), 0],
        ],
    ),
    (
        "observable-continuation",
        SOURCE / "observe_continuation.mpy",
        observe_python,
        [[0], [3, 4, 5, 1, 2], [3, 5, 4, 1, 2], [-1, -3, -2]],
    ),
    (
        "body-mutation",
        SOURCE / "body_mutation.mpy",
        body_python,
        [[0], [3, 4, 5, 1, 2], [3, 5, 4, 1, 2], [-1, -3, -2]],
    ),
]

checks = 0
for name, program, python_entry, cases in programs:
    for values in cases:
        expected = python_entry(values.copy())
        _, accelerated = run_krun(program, ORIGINAL_DEF, values)
        _, generic = run_krun(program, GENERIC_DEF, values)
        print(
            f"CASE name={name} input={values} "
            f"python={expected!r} accelerated={accelerated!r} generic={generic!r}"
        )
        if accelerated != expected or generic != expected:
            raise AssertionError((name, values, expected, accelerated, generic))
        checks += 1

print(f"CONCRETE_CHECKS={checks}")
print("MISMATCH_COUNT=0")
