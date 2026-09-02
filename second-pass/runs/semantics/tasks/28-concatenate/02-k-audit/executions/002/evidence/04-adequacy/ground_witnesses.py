#!/usr/bin/env python3
"""Ground witnesses for the candidate claims and their intended results."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.concatenate


canonical = load(Path("/reference/canonical.py"), "canonical_ground")
candidate = load(
    Path("/tmp/audit-work/28-concatenate-audit/solution.py"),
    "candidate_ground",
)

# Each case supplies a realizable function entry. In the corresponding loop
# witness, A starts as the empty code sequence, OLD_STRING starts as the empty
# string, ARGUMENT is the list value, and VS is its ValSeq.
cases = [
    [],
    ["a", "b", "c"],
    ["x", "", "y"],
    ["λ", "🙂"],
]

for strings in cases:
    oracle = canonical(strings)
    subject = candidate(strings)
    folded = ""
    last = ""
    for string in strings:
        folded += string
        last = string
    print(
        f"input={strings!r} canonical={oracle!r} candidate={subject!r} "
        f"loop_fold={folded!r} final_loop_value={last!r}"
    )
    assert oracle == subject == folded

print("GROUND_WITNESSES_PASS")
