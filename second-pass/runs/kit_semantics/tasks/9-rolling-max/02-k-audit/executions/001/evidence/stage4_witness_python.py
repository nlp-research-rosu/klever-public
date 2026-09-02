#!/usr/bin/env python3
"""Ground substitutions used for Stage 4 adequacy checks."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rolling_max


canonical = load("canonical_witness", Path("/reference/canonical.py"))
generated = load(
    "generated_witness",
    Path("/tmp/audit-work/rolling-max-20260729/solution.py"),
)

entry_cases = [[], [1, -2, 3, 2]]
expected = [[], [1, 1, 3, 3]]
for case, wanted in zip(entry_cases, expected):
    canonical_result = canonical(list(case))
    generated_result = generated(list(case))
    print(
        f"entry_input={case!r} expected={wanted!r} "
        f"canonical={canonical_result!r} generated={generated_result!r}"
    )
    assert canonical_result == generated_result == wanted

accumulator = [1]
current = 1
number = 1
remaining = [2, -1, 3]
for number in remaining:
    if number > current:
        current = number
    accumulator.append(current)
print(
    f"loop_start_A={[1]!r} M=1 D=1 remaining={remaining!r} "
    f"final_A={accumulator!r} final_M={current} final_D={number}"
)
assert accumulator == [1, 2, 2, 3]
assert current == 3
assert number == 3
