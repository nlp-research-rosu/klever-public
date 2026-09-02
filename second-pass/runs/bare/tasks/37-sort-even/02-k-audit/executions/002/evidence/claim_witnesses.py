#!/usr/bin/env python3
"""Concrete satisfying witnesses for every reachability claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load(Path("/tmp/audit-work/37-sort-even/solution.py"), "candidate_witness")
canonical = load(Path("/reference/canonical.py"), "canonical_witness")

entry_witnesses = [
    ("empty-example", [], []),
    ("prompt-example", [5, 6, 3, 4], [3, 6, 5, 4]),
    ("first-prompt-example", [1, 2, 3], [1, 2, 3]),
    ("symbolic-four-ordered", [1, 9, 3, 8], [1, 9, 3, 8]),
    ("symbolic-four-reversed", [5, 6, 3, 4], [3, 6, 5, 4]),
    ("top-correct", [9, 8, -1, 7, 3], [-1, 8, 3, 7, 9]),
]
for label, value, expected in entry_witnesses:
    generated = candidate.sort_even(list(value))
    trusted = canonical.sort_even(list(value))
    assert generated == trusted == expected
    print(
        f"{label}: input={value!r} candidate={generated!r} "
        f"canonical={trusted!r} satisfying=True"
    )

helper_witnesses = [
    ("even-correct", candidate.even_values, ([5, 6, 3, 4],), [5, 3]),
    ("insert-correct", candidate.insert_sorted, (3, [1, 4]), [1, 3, 4]),
    ("sort-correct", candidate.sort_values, ([5, 3, 4],), [3, 4, 5]),
    ("rebuild-correct", candidate.rebuild, ([5, 6, 3, 4], [3, 5]), [3, 6, 5, 4]),
]
for label, function, arguments, expected in helper_witnesses:
    actual = function(*arguments)
    assert actual == expected
    print(
        f"{label}: arguments={arguments!r} helper_result={actual!r} "
        f"claimed_reference={expected!r} satisfying=True"
    )

print("witness_count=10 failures=0")
