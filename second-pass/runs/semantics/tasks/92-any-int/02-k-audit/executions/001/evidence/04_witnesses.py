#!/usr/bin/env python3
"""Concrete satisfying witnesses for each entry claim and the Bool model gap."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_witness", "/reference/canonical.py")
generated = load("generated_witness", "/tmp/audit-work/reconstruction/solution.py")

witnesses = [
    # label, claim, args, K postcondition evaluated independently
    ("all_ints", 1, (5, 2, 7), True),
    ("x_nonint", 2, (1.5, 2, 3), False),
    ("y_nonint", 3, (1, 2.5, 3), False),
    ("z_nonint", 4, (1, 2, 3.5), False),
    # K Bool is a Val but isIntV(true) reduces to false, so claim 2 includes it.
    ("bool_false_conclusion_witness", 2, (True, 1, 2), False),
]

for label, claim, args, k_post in witnesses:
    canonical_result = canonical.any_int(*args)
    generated_result = generated.any_int(*args)
    print(
        f"{label}: claim={claim} args={args!r} "
        f"k_claimed={k_post!r} canonical={canonical_result!r} "
        f"generated={generated_result!r}"
    )
