#!/usr/bin/env python3
"""Run fresh K semantics and compare each result with both Python programs."""

from __future__ import annotations

import importlib.util
import pathlib
import re
import shlex
import subprocess
import sys
from types import ModuleType


def load_module(name: str, path: pathlib.Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_k_result(output: str) -> list[int]:
    match = re.search(r"<result>\s*(.*?)\s*</result>", output, re.DOTALL)
    if not match:
        raise ValueError("missing <result> cell")
    body = match.group(1)
    if "nil" not in body:
        raise ValueError(f"result is not a terminated PList: {body!r}")
    return [int(value) for value in re.findall(r"cons\s*\(\s*(-?\d+)", body)]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} SCRATCH_ROOT")
        return 64

    scratch = pathlib.Path(sys.argv[1]).resolve()
    canonical = load_module("trusted_canonical_k_compare", scratch / "canonical.py")
    submitted = load_module("submitted_solution_k_compare", scratch / "solution.py")
    cases = [0, 1, 2, 3, 4, 5, 10, 11, 18, 20, 26, 50]
    failures: list[str] = []

    print(f"scratch={scratch}")
    print(f"cases={cases}")
    for n in cases:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "semantic-fresh-kompiled",
            f"-cN={n}",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=scratch,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"\nCASE n={n}")
        print("COMMAND: " + shlex.join(command))
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
        print(f"EXIT_STATUS: {completed.returncode}")
        if completed.returncode != 0:
            failures.append(f"n={n}: krun exit {completed.returncode}")
            continue
        try:
            k_result = parse_k_result(completed.stdout)
        except ValueError as error:
            failures.append(f"n={n}: {error}")
            continue
        canonical_result = canonical.count_up_to(n)
        submitted_result = submitted.count_up_to(n)
        print(f"K_RESULT: {k_result}")
        print(f"CANONICAL_RESULT: {canonical_result}")
        print(f"SUBMITTED_PYTHON_RESULT: {submitted_result}")
        if "<k>\n    .K\n  </k>" not in completed.stdout:
            failures.append(f"n={n}: non-final <k> cell")
        if not (k_result == canonical_result == submitted_result):
            failures.append(
                f"n={n}: K={k_result} canonical={canonical_result} "
                f"submitted={submitted_result}"
            )

    print(f"\nfailure_count={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
