#!/usr/bin/env python3
"""Concrete satisfying witnesses for the entry and loop claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


canonical = load_entry(
    Path("/tmp/audit-work/review/trusted/canonical.py"), "claim_witness_canonical"
)
candidate = load_entry(
    Path("/tmp/audit-work/review/candidate-src/solution.py"),
    "claim_witness_candidate",
)


def overlap_count(source: str, pattern: str) -> int:
    if pattern == "":
        return len(source) + 1
    return sum(
        source[index : index + len(pattern)] == pattern
        for index in range(len(source))
    )


entry_witnesses = [
    ("aaaa", "aa", 3),
    ("abc", "", 4),
    ("", "a", 0),
]
for source, pattern, expected in entry_witnesses:
    summary = overlap_count(source, pattern)
    trusted = canonical(source, pattern)
    actual = candidate(source, pattern)
    print(
        "ENTRY_WITNESS",
        repr(source),
        repr(pattern),
        f"formal_summary={summary}",
        f"canonical={trusted}",
        f"candidate={actual}",
        f"expected={expected}",
    )
    assert summary == trusted == actual == expected

# SPEC.loop-inv witness:
# L=1, PAR=parent(0), string="aa", substring="a", count=5.
# Its only explicit requires-clause is that substring is nonempty.
loop_source = "aa"
loop_pattern = "a"
initial_count = 5
expected_final_count = initial_count + overlap_count(loop_source, loop_pattern)
print(
    "LOOP_WITNESS",
    "L=1",
    "PAR=parent(0)",
    f"string={loop_source!r}",
    f"substring={loop_pattern!r}",
    f"count={initial_count}",
    "requires_nonempty_pattern=True",
    "expected_final_string=''",
    f"expected_final_count={expected_final_count}",
)
assert loop_pattern != ""
assert expected_final_count == 7
print("CLAIM_WITNESSES_EXIT=0")
