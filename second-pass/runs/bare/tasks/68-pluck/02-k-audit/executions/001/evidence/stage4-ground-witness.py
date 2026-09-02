#!/usr/bin/env python3
"""Ground instances of the entry claim's VArray precondition."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


canonical = load_function(Path("/tmp/audit-work/trusted/canonical.py"), "witness_canonical")
candidate = load_function(
    Path("/tmp/audit-work/candidate-source/solution.py"), "witness_candidate"
)
program = "/tmp/audit-work/candidate-source/solution.mpy"
definition = "/tmp/audit-work/build/array-witness-kompiled"
cases = [
    (68, [4, 2, 3]),
    (69, []),
    (70, [7, 5, 9]),
    (71, [2, 2]),
    (72, [5, 0, 3, 0, 4, 2]),
]


def parse_result(stdout: str) -> list[int]:
    k_cell = re.search(r"<k>\s*(.*?)\s*</k>", stdout, re.DOTALL)
    if k_cell is None or k_cell.group(1).strip() != ".K":
        raise ValueError("nonterminal K cell")
    match = re.search(r"<result>\s*VList\s*\((.*?)\.Ints\s*\)\s*</result>", stdout, re.DOTALL)
    if match is None:
        raise ValueError("no VList result")
    prefix = match.group(1).strip().strip(",").strip()
    return [] if not prefix else [int(piece.strip()) for piece in prefix.split(",")]


failures = 0
for array_id, values in cases:
    command = [
        "krun",
        program,
        "--definition",
        definition,
        f"-cARGS=VArray({array_id},0,{len(values)})",
    ]
    print("$ " + shlex.join(command))
    run = subprocess.run(command, text=True, capture_output=True)
    print(run.stdout, end="")
    print(run.stderr, end="")
    print(f"[exit status: {run.returncode}]")
    try:
        k_result = parse_result(run.stdout)
    except Exception as err:
        k_result = f"ERROR: {err}"
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    equal = (
        run.returncode == 0
        and k_result == canonical_result
        and k_result == candidate_result
    )
    print(
        f"SATISFYING INSTANCE ID={array_id} OFFSET=0 LENGTH={len(values)} "
        f"array={values!r} K={k_result!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r} equal={equal}"
    )
    failures += not equal

print(f"SUMMARY satisfying_instances={len(cases)} failures={failures}")
raise SystemExit(1 if failures else 0)
