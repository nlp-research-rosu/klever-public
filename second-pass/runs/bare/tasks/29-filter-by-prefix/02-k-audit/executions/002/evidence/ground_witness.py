#!/usr/bin/env python3
"""Concrete satisfying witnesses for the two reachability preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


canonical = load_function(
    Path("/tmp/audit-work/29-filter-by-prefix/trusted/canonical.py"),
    "trusted_canonical_29_ground",
)
candidate = load_function(
    Path("/tmp/audit-work/29-filter-by-prefix/candidate-src/solution.py"),
    "candidate_solution_29_ground",
)

entry_input = ["abc", "bcd", "cde", "array"]
entry_prefix = "a"
entry_expected = ["abc", "array"]
print(
    "program-correct witness: "
    "env=.Map functions=.Map input="
    f"{entry_input!r} prefix={entry_prefix!r} output=noOutput"
)
print(f"trusted canonical result={canonical(list(entry_input), entry_prefix)!r}")
print(f"candidate Python result={candidate(list(entry_input), entry_prefix)!r}")
print(f"claimed K result={entry_expected!r}")
assert canonical(list(entry_input), entry_prefix) == entry_expected
assert candidate(list(entry_input), entry_prefix) == entry_expected

loop_input = ["abc", "bcd"]
loop_prefix = "a"
loop_accumulator = ["seed"]
loop_expected = loop_accumulator + canonical(loop_input, loop_prefix)
print(
    "loop-correct witness: "
    f"input={loop_input!r} prefix={loop_prefix!r} accumulator={loop_accumulator!r} "
    "restenv=.Map functions=.Map allinput=[] output=noOutput"
)
print(f"claimed filterAcc result={loop_expected!r}")
assert loop_expected == ["seed", "abc"]
