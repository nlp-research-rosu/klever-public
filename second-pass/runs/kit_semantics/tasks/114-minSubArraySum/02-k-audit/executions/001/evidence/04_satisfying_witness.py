#!/usr/bin/env python3
"""Ground witnesses for SPEC.loop-invariant and SPEC.target preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
generated = load(
    Path("/tmp/audit-work/114-minSubArraySum/solution.py"),
    "generated_witness",
)


def claimed_summary(
    values: list[int], current: int, minimum: int
) -> tuple[int, int]:
    """The literal kadaneCurrent/kadaneMinimum equations from verification.k."""
    for value in values:
        next_current = min(value, current + value)
        minimum = min(minimum, next_current)
        current = next_current
    return current, minimum


loop_values = [-2, 4, -7]
loop_current, loop_minimum = claimed_summary(loop_values, 1, 3)
print(
    "LOOP_WITNESS:",
    {
        "VS": loop_values,
        "C": 1,
        "B": 3,
        "MODULE": {},
        "min_absent": True,
        "allInts": True,
        "post_current": loop_current,
        "post_minimum": loop_minimum,
    },
)
assert (loop_current, loop_minimum) == (-7, -7)

for values in ([5], [3, -4, 2], [-1, -2, -3]):
    summary = claimed_summary(values, 0, values[0])[1]
    c = canonical(list(values))
    g = generated(list(values))
    print(
        "TARGET_WITNESS:",
        {
            "H": values[0],
            "XS": list(values[1:]),
            "allInts_XS": True,
            "claimed_kadaneMinimum": summary,
            "canonical": c,
            "generated": g,
        },
    )
    assert summary == c == g
