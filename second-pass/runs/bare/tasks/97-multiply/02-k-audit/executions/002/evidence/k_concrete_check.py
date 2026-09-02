#!/usr/bin/env python3
"""Compare fresh generated-semantics runs with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
DEFINITION = ROOT / "semantic-kompiled"


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


canonical = load_function(ROOT / "canonical.py", "kcheck_canonical")
generated = load_function(ROOT / "solution.py", "kcheck_generated")

cases = [
    (148, 412),
    (19, 28),
    (2020, 1851),
    (14, -15),
    (0, 0),
    (-1, 1),
    (1, -1),
    (-1, -1),
    (-9, 9),
    (-10, 11),
    (-11, 1),
    (10**40 + 7, -(10**40 + 8)),
]

k_generated_mismatches = []
k_canonical_mismatches = []
for a, b in cases:
    command = [
        "krun",
        "regenerated-solution.mpy",
        f"-cA={a}",
        f"-cB={b}",
        "--definition",
        str(DEFINITION),
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    print("KRUN_EXIT:", completed.returncode)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        raise SystemExit(completed.returncode)
    match = re.search(r"<result>\s*(-?[0-9]+)\s*</result>", completed.stdout)
    if match is None:
        print(completed.stdout)
        raise SystemExit("could not parse <result> from krun output")
    k_result = int(match.group(1))
    generated_result = generated(a, b)
    canonical_result = canonical(a, b)
    print(
        f"CASE a={a} b={b} K={k_result} "
        f"generated={generated_result} canonical={canonical_result}"
    )
    if k_result != generated_result:
        k_generated_mismatches.append((a, b, k_result, generated_result))
    if k_result != canonical_result:
        k_canonical_mismatches.append((a, b, k_result, canonical_result))

print(f"K_VS_GENERATED_MISMATCHES: {len(k_generated_mismatches)}")
print(f"K_VS_CANONICAL_MISMATCHES: {len(k_canonical_mismatches)}")
if k_canonical_mismatches:
    print("K_VS_CANONICAL_WITNESSES:", k_canonical_mismatches)
if k_generated_mismatches:
    print("K_VS_GENERATED_WITNESSES:", k_generated_mismatches)
    raise SystemExit(1)
print("GENERATED_SEMANTICS_CONCRETE_CHECK: PASS_FOR_GENERATED_PROGRAM")
