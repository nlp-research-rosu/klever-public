#!/usr/bin/env python3
"""Compare fresh generated-semantics executions against two Python oracles."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable


REBUILD = Path("/tmp/audit-work/rebuild")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


candidate = load_entry(REBUILD / "solution.py", "candidate_concrete")
canonical = load_entry(
    Path("/tmp/audit-work/reference/canonical.py"), "canonical_concrete"
)

cases = [
    [],
    [7],
    [1, 2],
    [1, 1],
    [1, 2, 3, 2, 4],
    [1, 1, 1],
    [-1, 0, -1, 2],
    [3, 1, 3, 2, 1, 4, 2, 5],
    [10**30, -(10**30), 10**30, 7],
]


def k_input(values: list[int]) -> str:
    return "listValue(" + ", ".join(map(str, values)) + ")"


def parse_output(text: str) -> list[int]:
    match = re.search(
        r"<output>\s*listValue\s*\((.*?)\)\s*</output>", text, re.DOTALL
    )
    if match is None:
        raise RuntimeError(f"missing output cell in:\n{text}")
    payload = match.group(1)
    payload = re.sub(r",?\s*\.Ints\s*$", "", payload).strip()
    if not payload:
        return []
    return [int(piece.strip()) for piece in payload.split(",")]


mismatches = 0
for values in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "semantic-kompiled",
        f"-cINPUT={k_input(values)}",
    ]
    print("COMMAND: " + shlex.join(command))
    result = subprocess.run(
        command,
        cwd=REBUILD,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"KRUN_EXIT_STATUS: {result.returncode}")
    if result.returncode != 0:
        print(result.stdout[-4000:])
        raise SystemExit(result.returncode)
    k_result = parse_output(result.stdout)
    candidate_result = candidate(list(values))
    canonical_result = canonical(list(values))
    matches = k_result == candidate_result == canonical_result
    print(
        f"input={values!r} k={k_result!r} candidate={candidate_result!r} "
        f"canonical={canonical_result!r} matches={matches}"
    )
    if not matches:
        mismatches += 1

print(f"case_count={len(cases)}")
print(f"mismatch_count={mismatches}")
if mismatches:
    raise SystemExit(1)
