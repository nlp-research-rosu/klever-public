#!/usr/bin/env python3
"""Execute the clean generated semantics and compare results with Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shlex
import subprocess
from typing import Callable


DEFINITION = Path("/tmp/audit-work/candidate/semantics-kompiled")
PROGRAM = Path("/tmp/audit-work/candidate/solution.mpy")
SOLUTION = Path("/tmp/audit-work/candidate/solution.py")
CANONICAL = Path("/tmp/audit-work/trusted/canonical.py")


def load_entry(path: Path, name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique


def k_list(values: list[int]) -> str:
    return "ListExpr(" + ", ".join(f"Int({value})" for value in values) + ")"


def parsed_vints(output: str) -> list[int]:
    return [int(value) for value in re.findall(r"VInt \( (-?[0-9]+) \)", output)]


def main() -> None:
    solution = load_entry(SOLUTION, "concrete_generated_solution")
    canonical = load_entry(CANONICAL, "concrete_trusted_canonical")
    cases = [
        ("documented-example", [5, 3, 5, 2, 3, 3, 9, 0, 123]),
        ("empty", []),
        ("singleton", [7]),
        ("all-equal", [4, 4, 4, 4]),
        ("equality-and-order-branches", [2, -1, 2, 0, -1, 1]),
        ("extreme-integers", [10**80, -(10**80), 0, 10**80]),
    ]
    for name, values in cases:
        argument = k_list(values)
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cARGS={argument}",
        ]
        print("CASE", name)
        print("COMMAND", shlex.join(command))
        result = subprocess.run(command, capture_output=True, text=True)
        combined = result.stdout + result.stderr
        print("OUTPUT")
        print(combined, end="" if combined.endswith("\n") else "\n")
        print("EXIT_STATUS", result.returncode)
        expected = canonical(list(values))
        candidate = solution(list(values))
        actual = parsed_vints(combined)
        print(
            f"COMPARE python_canonical={expected!r} "
            f"python_candidate={candidate!r} k={actual!r}"
        )
        if result.returncode != 0:
            raise SystemExit(f"krun failed for {name}")
        if actual != expected or candidate != expected:
            raise SystemExit(f"semantic mismatch for {name}")
    print(f"CONCRETE_CASES {len(cases)}")
    print("MISMATCHES 0")


if __name__ == "__main__":
    main()
