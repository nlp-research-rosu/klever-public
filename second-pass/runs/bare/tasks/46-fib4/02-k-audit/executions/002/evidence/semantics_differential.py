#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with two independent Python runs."""

from __future__ import annotations

import importlib.util
import random
import re
import subprocess
from pathlib import Path
from types import ModuleType


WORK = Path("/tmp/audit-work/46-fib4")
RESULT = re.compile(r"<result>\s*result\s*\(\s*(-?\d+)\s*\)\s*</result>", re.DOTALL)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical_semantics_check", Path("/reference/canonical.py"))
candidate = load_module("candidate_semantics_check", Path("/candidate/solution.py"))

rng = random.Random(464646)
inputs = list(dict.fromkeys([0, 1, 2, 3, 4, 5, 6, 7, 10, 20] + list(range(0, 31)) + [
    rng.randrange(0, 101) for _ in range(10)
]))
mismatches: list[str] = []
for n in inputs:
    process = subprocess.run(
        [
            "krun",
            "solution.mpy",
            f"-cARG={n}",
            "--definition",
            "concrete-kompiled",
        ],
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    match = RESULT.search(process.stdout)
    if process.returncode != 0 or match is None:
        mismatches.append(
            f"n={n} krun_exit={process.returncode} parse={match is not None} "
            f"output={process.stdout!r}"
        )
        continue
    k_value = int(match.group(1))
    canonical_value = canonical.fib4(n)
    candidate_value = candidate.fib4(n)
    if not (k_value == canonical_value == candidate_value):
        mismatches.append(
            f"n={n} k={k_value} canonical={canonical_value} candidate={candidate_value}"
        )

print("semantics_inputs=" + ",".join(map(str, inputs)))
print(f"semantics_test_count={len(inputs)}")
print(f"semantics_mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH " + mismatch)
if mismatches:
    raise SystemExit(1)
