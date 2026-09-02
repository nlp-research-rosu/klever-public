#!/usr/bin/env python3
"""Concrete satisfying witnesses for all eight positive K claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


def load(path: str):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


canonical = load("/reference/canonical.py")
generated = load("/candidate/solution.py")


def strict_max(seed: Any, rest: list[Any]) -> Any:
    candidate = seed
    for value in rest:
        if value > candidate:
            candidate = value
    return candidate


witnesses = [
    ("SPEC.max-int-numeric-acc", 1, [2, -3], strict_max(1, [2, -3])),
    ("SPEC.max-float-numeric-acc", 1.5, [-2, 3.25], strict_max(1.5, [-2, 3.25])),
    ("SPEC.max-general-numeric-acc", False, [True, 0.5], strict_max(False, [True, 0.5])),
    ("SPEC.max-element-int-head", 1, [2, -3], strict_max(1, [2, -3])),
    ("SPEC.max-element-float-head", 1.5, [-2, 3.25], strict_max(1.5, [-2, 3.25])),
    ("SPEC.max-element-bool-head", False, [True, False], strict_max(False, [True, False])),
    ("SPEC-STR.max-general-str-acc", "ant", ["zebra", "yak"], strict_max("ant", ["zebra", "yak"])),
    ("SPEC-STR.max-element-str-head", "ant", ["zebra", "yak"], strict_max("ant", ["zebra", "yak"])),
]

for claim, seed, rest, claimed in witnesses:
    full = [seed, *rest]
    row = {
        "claim": claim,
        "seed": seed,
        "rest": rest,
        "precondition_satisfied": (
            all(isinstance(x, (int, float, bool)) for x in full)
            if not isinstance(seed, str)
            else all(isinstance(x, str) for x in full)
        ),
        "claimed_summary": claimed,
        "canonical": canonical(full),
        "generated": generated(full),
    }
    row["all_equal"] = (
        row["claimed_summary"] == row["canonical"] == row["generated"]
    )
    print(repr(row))
    assert row["precondition_satisfied"] and row["all_equal"]
