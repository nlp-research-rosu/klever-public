#!/usr/bin/env python3
"""Ground satisfying-input accounting for the K entry and loop claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


canonical = load("canonical_stage4", "/reference/canonical.py")
generated = load(
    "generated_stage4", "/tmp/audit-work/132-is-nested/source/solution.py"
)


def scan_state(value: str, initial: int = 0) -> int:
    state = initial
    for char in value:
        if char == "[":
            state = state + 1 if state < 2 else state
        else:
            state = state + 1 if state > 1 and state < 4 else state
    return state


witnesses = [
    ("loop-empty", "", 0, False),
    ("entry-empty", "", 0, False),
    ("entry-nested", "[[]]", 0, True),
]

for name, value, initial, claimed in witnesses:
    summary = scan_state(value, initial) == 4
    canonical_result = canonical(value)
    generated_result = generated(value)
    print(
        f"{name}: input={value!r} initial={initial} "
        f"scanState==4={summary} canonical={canonical_result} "
        f"generated={generated_result} claimed={claimed}"
    )
    assert summary == claimed
    assert canonical_result == claimed
    assert generated_result == claimed
