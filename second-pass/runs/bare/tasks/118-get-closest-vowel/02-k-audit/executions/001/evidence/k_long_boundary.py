#!/usr/bin/env python3
"""Compare K's unbounded call stack with real CPython at length 1000."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def python_outcome(function, word: str):
    try:
        return ("return", function(word))
    except BaseException as error:
        return ("raise", type(error).__name__, str(error))


def parse_k_result(stdout: str) -> str:
    k_cell_match = re.search(r"<k>\s*(.*?)\s*</k>", stdout, re.DOTALL)
    if not k_cell_match:
        raise ValueError("no <k> cell in krun output")
    k_cell = " ".join(k_cell_match.group(1).split())
    if re.fullmatch(r"pyStr \( \.Chars \) ~> \.K", k_cell):
        return ""
    raise ValueError(f"unexpected final <k> cell: {k_cell}")


def main() -> int:
    word = "b" * 1000
    canonical = load_entry("trusted_canonical_klong", Path("/reference/canonical.py"))
    candidate = load_entry(
        "scratch_candidate_klong", Path("/tmp/audit-work/candidate-src/solution.py")
    )
    command = [
        "krun",
        "solution.fresh.mpy",
        f'-cARG=word("{word}")',
        "--definition",
        "concrete-kompiled",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd="/tmp/audit-work/build-concrete",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    print("INPUT: word = 'b' * 1000")
    print(
        "COMMAND: (cd /tmp/audit-work/build-concrete && "
        "krun solution.fresh.mpy -cARG='word(\"<1000 b characters>\")' "
        "--definition concrete-kompiled --output pretty)"
    )
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    if completed.returncode:
        print(f"KRUN_STDOUT_TAIL: {completed.stdout[-1000:]}")
        print(f"KRUN_STDERR_TAIL: {completed.stderr[-1000:]}")
        return 2
    k_value = parse_k_result(completed.stdout)
    canonical_value = python_outcome(canonical, word)
    candidate_value = python_outcome(candidate, word)
    print(f"K_RESULT: {k_value!r}")
    print(f"CANONICAL_PYTHON: {canonical_value!r}")
    print(f"CANDIDATE_PYTHON: {candidate_value!r}")
    mismatch = candidate_value != ("return", k_value)
    print(f"K_VS_CANDIDATE_MISMATCH: {mismatch}")
    return 1 if mismatch else 0


if __name__ == "__main__":
    raise SystemExit(main())
