#!/usr/bin/env python3
"""Concrete substitutions for the entry-claim empty and cons partitions."""

from __future__ import annotations

import importlib.util


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load("ground_candidate", "/candidate/solution.py")
canonical = load("ground_canonical", "/reference/canonical.py")

cases = [
    [],
    ["1"],
    ["1234567"],
    ["", "135791357913"],
]
for values in cases:
    candidate_value = candidate.odd_count(values)
    canonical_value = canonical.odd_count(values)
    print(
        f"INPUT={values!r} CANDIDATE={candidate_value!r} "
        f"CANONICAL={canonical_value!r} EQUAL={candidate_value == canonical_value}"
    )
