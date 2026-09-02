#!/usr/bin/env python3
"""Probe literal-list inputs excluded by the K claim's Ints precondition."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


def outcome(function, left, right):
    try:
        return ("return", function(left, right))
    except Exception as error:  # This probe intentionally compares exceptions.
        return ("raise", type(error).__name__, str(error))


canonical = load(Path("/reference/canonical.py"), "canonical_edge")
generated = load(Path("/tmp/audit-work/58-common/solution.py"), "generated_edge")

nan_value = float("nan")
cases = [
    ("disjoint unhashable values", [[1]], [[2]]),
    ("unhashable left versus empty", [[1]], []),
    ("empty versus unhashable right", [], [[2]]),
    ("same NaN object", [nan_value], [nan_value]),
]

mismatches = 0
for label, left, right in cases:
    expected = outcome(canonical, left, right)
    actual = outcome(generated, left, right)
    matched = (
        expected[0] == actual[0]
        and (
            expected == actual
            or (
                expected[0] == "return"
                and len(expected[1]) == len(actual[1])
                and all(
                    (math.isnan(e) and math.isnan(a)) if isinstance(e, float)
                    else e == a
                    for e, a in zip(expected[1], actual[1])
                )
            )
        )
    )
    print(
        f"LABEL={label!r} LEFT={left!r} RIGHT={right!r} "
        f"CANONICAL={expected!r} GENERATED={actual!r} MATCH={matched}"
    )
    mismatches += int(not matched)

print(f"CASE_COUNT={len(cases)} MISMATCH_COUNT={mismatches}")
# Mismatches are the expected evidence: these inputs are outside the formal
# Ints domain but inside the prompt's unqualified Python `list` annotation.
raise SystemExit(0 if mismatches == len(cases) else 1)
