#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare with two Python oracles."""

from __future__ import annotations

import importlib.util
import os
import re
import shlex
import subprocess
from pathlib import Path

PROGRAM = Path("/tmp/audit-work/source/solution.mpy")
DEFINITION = Path(
    os.environ.get(
        "CONCRETE_DEFINITION",
        "/tmp/audit-work/build/semantic-llvm-kompiled",
    )
)
CASES = [
    [2, 3, 4, 1, 2, 4],
    [-1, -2, -3],
    [7],
    [0],
    [-11],
    [4, -5],
    [5, -2, -3, 7, -10, 4],
    [1, -2, 1, -3],
]


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


def int_list(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return result


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_concrete")
    generated = load_entry(Path("/tmp/audit-work/source/solution.py"), "generated_concrete")
    failures = 0
    for index, values in enumerate(CASES, 1):
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            '-cENTRY="minSubArraySum"',
            f"-cARGS=pyList({int_list(values)})",
        ]
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=120,
        )
        match = re.search(
            r"<k>\s*pyInt\s*\(\s*(-?[0-9]+)\s*\)"
            r"(?:\s*~>\s*\.K)?\s*</k>",
            completed.stdout,
            re.DOTALL,
        )
        k_value = int(match.group(1)) if match else None
        canonical_value = canonical(list(values))
        generated_value = generated(list(values))
        agrees = (
            completed.returncode == 0
            and k_value == canonical_value
            and k_value == generated_value
        )
        print(f"CASE {index}")
        print(f"input={values!r}")
        print(f"command={shlex.join(command)}")
        print(f"exit_status={completed.returncode}")
        print(f"k_value={k_value!r}")
        print(f"canonical_value={canonical_value!r}")
        print(f"generated_value={generated_value!r}")
        print(f"agrees={agrees}")
        print("krun_output_begin")
        print(completed.stdout.rstrip())
        print("krun_output_end")
        if not agrees:
            failures += 1
    print(f"cases={len(CASES)}")
    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
