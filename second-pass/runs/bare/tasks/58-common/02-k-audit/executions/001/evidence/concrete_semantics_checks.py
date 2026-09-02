#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare with Python."""

from __future__ import annotations

import importlib.util
import os
import re
import shlex
import subprocess
from pathlib import Path


def load_common(path: Path):
    spec = importlib.util.spec_from_file_location("canonical_for_krun", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


def k_list(values: list[int]) -> str:
    return "list(" + ",".join(str(value) for value in values) + ")"


def result_from_krun(output: str) -> list[int]:
    match = re.search(r"<k>(.*?)</k>", output, flags=re.DOTALL)
    if match is None:
        raise ValueError("krun output lacks a <k> cell")
    k_cell = match.group(1)
    if "list" not in k_cell or "~> .K" not in k_cell:
        raise ValueError(f"unexpected final <k> cell: {k_cell!r}")
    return [int(token) for token in re.findall(r"-?\d+", k_cell)]


work = Path("/tmp/audit-work/58-common")
canonical = load_common(Path("/reference/canonical.py"))
cases = [
    ([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121]),
    ([5, 3, 2, 8], [3, 2]),
    ([], []),
    ([], [0, 0]),
    ([0, 1], []),
    ([3, 3, -1, 2], [3, -1, -1]),
    ([4, 1, 3, 2], [4, 1, 3, 2]),
    ([10**50, -(10**50), 0], [10**50, -(10**50)]),
]

environment = dict(os.environ)
environment["PATH"] = "/home/agent/.nix-profile/bin:" + environment["PATH"]
mismatches = 0

for index, (left, right) in enumerate(cases):
    command = [
        "krun",
        str(work / "regenerated-solution.mpy"),
        "--definition",
        str(work / "semantic-kompiled"),
        "-cL1=" + k_list(left),
        "-cL2=" + k_list(right),
    ]
    print(f"CASE {index} COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=work,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    print(f"CASE {index} EXIT_STATUS: {completed.returncode}")
    expected = canonical(list(left), list(right))
    actual = result_from_krun(completed.stdout) if completed.returncode == 0 else None
    matched = completed.returncode == 0 and actual == expected
    print(
        f"CASE {index} PYTHON_RESULT={expected!r} "
        f"K_RESULT={actual!r} MATCH={matched}"
    )
    if not matched:
        mismatches += 1

print(f"CASE_COUNT={len(cases)}")
print(f"MISMATCH_COUNT={mismatches}")
raise SystemExit(1 if mismatches else 0)
