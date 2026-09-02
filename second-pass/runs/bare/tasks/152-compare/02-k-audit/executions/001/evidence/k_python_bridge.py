#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with trusted Python."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/152-compare")


def load_entry(path: Path):
    spec = importlib.util.spec_from_file_location("canonical_bridge_oracle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare


def values_term(values: list[int]) -> str:
    tail = "VNil"
    for value in reversed(values):
        tail = f"VCons(VInt({value}), {tail})"
    return f"VList({tail})"


canonical = load_entry(SCRATCH / "trusted" / "canonical.py")
cases = [
    ([], []),
    ([0], [0]),
    ([0], [1]),
    ([1], [0]),
    ([-1], [0]),
    ([0], [-1]),
    ([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]),
    ([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]),
    ([-10**30, 0, 10**30], [10**30, 0, -10**30]),
]

mismatches = []
for index, (game, guess) in enumerate(cases):
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "semantic-audit-kompiled",
        f"-cGAME={values_term(game)}",
        f"-cGUESS={values_term(guess)}",
    ]
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"krun case {index} exited {completed.returncode}:\n{completed.stdout}"
        )
    k_result = [int(item) for item in re.findall(r"VInt \( (-?\d+) \)", completed.stdout)]
    python_result = canonical(game, guess)
    print(
        f"CASE {index}: game={game!r} guess={guess!r} "
        f"python={python_result!r} k={k_result!r}"
    )
    if k_result != python_result:
        mismatches.append(index)

print("CASES:", len(cases))
print("MISMATCH_COUNT:", len(mismatches))
if mismatches:
    raise SystemExit(1)
