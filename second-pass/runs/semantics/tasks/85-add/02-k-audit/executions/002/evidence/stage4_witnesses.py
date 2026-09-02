#!/usr/bin/env python3
"""Ground substitutions for the result appearing in the K entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/85-add")


def load_function(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


def add_acc_spec(values: list[int], phase: bool = False, acc: int = 0) -> int:
    for value in values:
        if phase and value % 2 == 0:
            acc += value
        phase = not phase
    return acc


canonical = load_function("trusted_canonical_witness", WORK / "canonical.py")
generated = load_function("candidate_generated_witness", WORK / "solution.py")
inputs = [
    [4, 2, 6, 7],
    [1, -2],
    [-2, -4, -6, -8],
    [1, 3, 4, -6, 8, 10],
]

print("$ python3 /audit-output/evidence/stage4_witnesses.py")
for values in inputs:
    summary = add_acc_spec(values)
    canonical_result = canonical(values)
    generated_result = generated(values)
    print(
        f"input={values!r} addAccSpec={summary} "
        f"canonical={canonical_result} generated={generated_result}"
    )
    assert summary == canonical_result == generated_result
print("witness_status=PASS")
print("[exit 0]")
