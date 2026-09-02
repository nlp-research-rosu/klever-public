#!/usr/bin/env python3
"""Run the rebuilt generated semantics and compare its output with Python."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/120-maximum/candidate")


def load_solution():
    spec = importlib.util.spec_from_file_location("generated_solution_for_k", ROOT / "solution.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import generated solution")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.maximum


def k_list(values: list[int]) -> str:
    items = " ".join(f"ListItem({value})" for value in values)
    return f"listVal({items if items else '.List'})"


def parse_out(stdout: str) -> list[int]:
    match = re.search(r"<out>\s*listVal\s*\((.*?)\)\s*</out>", stdout, re.DOTALL)
    if not match:
        raise ValueError(f"no final listVal in <out>; output sha256={hashlib.sha256(stdout.encode()).hexdigest()}")
    return [int(value) for value in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", match.group(1))]


def main() -> None:
    maximum = load_solution()
    length_1000 = [((index * 37) % 2001) - 1000 for index in range(1000)]
    cases = [
        ("example-1", [-3, -4, 5], 3),
        ("example-2", [4, -4, 4], 2),
        ("example-3", [-3, 2, 1, 2, -1, -2, 1], 1),
        ("k-zero", [7, -1], 0),
        ("k-equals-length", [7, -1], 2),
        ("singleton-lower-bound", [-1000], 1),
        ("element-bounds", [-1000, 1000, 0, 1000], 3),
        ("maximum-length", length_1000, 3),
    ]
    mismatches = 0
    for label, arr, k in cases:
        args = f"ListItem({k_list(arr)}) ListItem(intVal({k}))"
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "concrete-kompiled",
            f"-cARGS={args}",
        ]
        printable = shlex.join(command)
        if len(printable) > 1000:
            printable = printable[:700] + f"... <args_sha256={hashlib.sha256(args.encode()).hexdigest()}>"
        print(f"COMMAND {label}: {printable}")
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
            check=False,
        )
        print(
            f"RESULT {label}: exit={completed.returncode} "
            f"stdout_sha256={hashlib.sha256(completed.stdout.encode()).hexdigest()}"
        )
        if completed.returncode != 0:
            print(completed.stdout[-4000:])
            raise SystemExit(completed.returncode)
        actual = parse_out(completed.stdout)
        generated_python = maximum(list(arr), k)
        independent_oracle = sorted(arr)[len(arr) - k :] if k else []
        matches = actual == generated_python == independent_oracle
        print(
            f"COMPARE {label}: output_len={len(actual)} "
            f"output={actual if len(actual) <= 20 else actual[:10] + ['...'] + actual[-10:]} "
            f"match={matches}"
        )
        if not matches:
            mismatches += 1
    print(f"cases={len(cases)} mismatches={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
