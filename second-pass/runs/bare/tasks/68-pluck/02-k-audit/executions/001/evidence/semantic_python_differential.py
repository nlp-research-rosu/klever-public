#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


PROGRAM = Path("/tmp/audit-work/candidate-source/solution.mpy")
DEFINITION = Path("/tmp/audit-work/build/semantic-kompiled-fresh")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


canonical = load_function(Path("/tmp/audit-work/trusted/canonical.py"), "semantic_canonical")
candidate = load_function(
    Path("/tmp/audit-work/candidate-source/solution.py"), "semantic_candidate"
)

cases = [
    [4, 2, 3],
    [1, 2, 3],
    [],
    [5, 0, 3, 0, 4, 2],
    [7, 5, 9],
    [2, 2],
    [0],
    [9, 8],
]


def k_argument(case: list[int]) -> str:
    return "VList(" + ",".join(map(str, case)) + ")"


def parse_result(stdout: str) -> list[int]:
    k_cell = re.search(r"<k>\s*(.*?)\s*</k>", stdout, re.DOTALL)
    if k_cell is None or k_cell.group(1).strip() != ".K":
        raise ValueError("execution did not finish with an empty <k> cell")
    match = re.search(r"<result>\s*VList\s*\((.*?)\.Ints\s*\)\s*</result>", stdout, re.DOTALL)
    if match is None:
        raise ValueError("could not find a final VList result")
    prefix = match.group(1).strip().strip(",").strip()
    if not prefix:
        return []
    return [int(piece.strip()) for piece in prefix.split(",")]


failed = False
for case in cases:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cARGS={k_argument(case)}",
    ]
    print("$ " + shlex.join(command))
    run = subprocess.run(command, text=True, capture_output=True)
    print(run.stdout, end="")
    if run.stderr:
        print(run.stderr, end="")
    print(f"[exit status: {run.returncode}]")
    try:
        semantic_result = parse_result(run.stdout)
    except Exception as err:
        semantic_result = f"PARSE/TERMINATION ERROR: {err}"
    canonical_result = canonical(list(case))
    candidate_result = candidate(list(case))
    equal = (
        run.returncode == 0
        and semantic_result == canonical_result
        and semantic_result == candidate_result
    )
    print(
        f"COMPARE input={case!r} K={semantic_result!r} "
        f"canonical={canonical_result!r} candidate={candidate_result!r} equal={equal}"
    )
    failed |= not equal

print(f"SUMMARY cases={len(cases)} mismatches={int(failed)}")
raise SystemExit(1 if failed else 0)
