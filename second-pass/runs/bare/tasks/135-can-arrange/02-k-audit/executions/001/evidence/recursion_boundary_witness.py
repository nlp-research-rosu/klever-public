#!/usr/bin/env python3
"""Ground witness for the generated-semantics/CPython recursion discrepancy."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path


LENGTH = 997
PROGRAM = Path("/tmp/audit-work/135-can-arrange/source/solution.mpy")
DEFINITION = Path("/tmp/audit-work/135-can-arrange/build/concrete-kompiled")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


def observe(fn, arr: list[int]) -> str:
    try:
        return f"return {fn(list(arr))!r}"
    except BaseException as err:
        return f"exception {type(err).__name__}: {err}"


def main() -> int:
    arr = list(range(LENGTH))
    k_array = "seq(" + ",".join(str(value) for value in arr) + ")"
    command = [
        "krun",
        str(PROGRAM),
        f"-cARGS=arrayVal({k_array},0,{LENGTH})",
        "--definition",
        str(DEFINITION),
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    matches = re.findall(r"value \( intVal \( (-?\d+) \) \)", completed.stdout)
    k_result = int(matches[-1]) if matches else None

    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_recursion")
    generated = load_entry(
        Path("/tmp/audit-work/135-can-arrange/source/solution.py"),
        "submitted_solution_recursion",
    )
    canonical_observation = observe(canonical, arr)
    generated_observation = observe(generated, arr)

    print(f"INPUT: increasing unique integer array range(0, {LENGTH})")
    print(f"COMMAND: {shlex.join(command)}")
    print(f"K EXIT: {completed.returncode}")
    print(f"K RESULT: {k_result}")
    print(f"TRUSTED PYTHON: {canonical_observation}")
    print(f"SUBMITTED PYTHON: {generated_observation}")
    if completed.returncode != 0 or k_result is None:
        print("K STDOUT:")
        print(completed.stdout)
        print("K STDERR:")
        print(completed.stderr)
        return 2

    discrepancy_reproduced = (
        k_result == -1
        and canonical_observation == "return -1"
        and generated_observation.startswith("exception RecursionError:")
    )
    print(f"DISCREPANCY REPRODUCED: {discrepancy_reproduced}")
    return 0 if discrepancy_reproduced else 1


if __name__ == "__main__":
    sys.exit(main())
