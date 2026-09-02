#!/usr/bin/env python3
"""Compare fresh K concrete execution with both independent Python executions."""

from __future__ import annotations

import importlib.util
import pathlib
import re
import shlex
import subprocess


K_INPUTS = [0, 1, 9, 10, 11, 99, 100, 101, 147, 150, 999, 1000, 1001, 9999, 10000]
PROGRAM = pathlib.Path("/tmp/audit-work/src/solution.mpy")
DEFINITION = pathlib.Path("/tmp/audit-work/concrete-kompiled")
RESULT_RE = re.compile(r'VStr\s*\(\s*"([^"]*)"\s*\)')


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load_module("trusted_canonical_k_compare", pathlib.Path("/reference/canonical.py"))
    generated = load_module(
        "scratch_generated_k_compare", pathlib.Path("/tmp/audit-work/src/solution.py")
    )
    failures = 0
    print(f"inputs={K_INPUTS}")
    for n in K_INPUTS:
        command = [
            "/usr/bin/krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cN={n}",
        ]
        print(f"$ {shlex.join(command)}")
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        print(f"exit={completed.returncode}")
        if completed.stderr:
            print("stderr:")
            print(completed.stderr.rstrip())
        print("stdout:")
        print(completed.stdout.rstrip())
        matches = RESULT_RE.findall(completed.stdout)
        k_value = matches[-1] if matches else None
        canonical_value = canonical.solve(n)
        generated_value = generated.solve(n)
        agrees = (
            completed.returncode == 0
            and k_value == canonical_value
            and k_value == generated_value
        )
        print(
            f"comparison n={n} k={k_value!r} canonical={canonical_value!r} "
            f"generated={generated_value!r} agrees={agrees}"
        )
        if not agrees:
            failures += 1
    print(f"cases={len(K_INPUTS)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
