#!/usr/bin/env python3
"""Ground witnesses for the implicit sorted K claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


canonical = load("witness_canonical", SCRATCH / "trusted/canonical.py")
generated = load("witness_generated", SCRATCH / "solution.py")

witnesses = [
    # Both entry claims have no explicit requires. These instantiate all sorted
    # variables and satisfy their exact configuration patterns.
    {
        "name": "empty",
        "k_is": ".IntSeq",
        "values": [],
        "threshold": 0,
        "loop_original": ".IntSeq",
        "loop_old": 0,
        "builtins": "builtinsScope",
    },
    {
        "name": "equal-boundary",
        "k_is": "iCons(5, .IntSeq)",
        "values": [5],
        "threshold": 5,
        "loop_original": "iCons(5, .IntSeq)",
        "loop_old": 0,
        "builtins": "builtinsScope",
    },
    {
        "name": "all-below",
        "k_is": "iCons(-4, iCons(-10, .IntSeq))",
        "values": [-4, -10],
        "threshold": -3,
        "loop_original": "iCons(-4, iCons(-10, .IntSeq))",
        "loop_old": 0,
        "builtins": "builtinsScope",
    },
]

for witness in witnesses:
    values = witness["values"]
    threshold = witness["threshold"]
    formula = all(value < threshold for value in values)
    c_result = canonical(list(values), threshold)
    g_result = generated(list(values), threshold)
    print(
        f"{witness['name']}: IS={witness['k_is']} T={threshold} "
        f"ORIGINAL={witness['loop_original']} OLD={witness['loop_old']} "
        f"BUILTINS={witness['builtins']} "
        f"belowThresholdSpec={formula} canonical={c_result} generated={g_result}"
    )
    if not (formula is c_result is g_result):
        raise SystemExit(1)
