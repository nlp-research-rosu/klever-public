#!/usr/bin/env python3
"""Ground witnesses for every candidate entry claim and its intended result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


canonical = load(Path("/reference/canonical.py"), "claim_witness_canonical")
candidate = load(
    Path("/tmp/audit-work/111-histogram/solution.py"), "claim_witness_candidate"
)

witnesses = [
    (1, "", {}),
    (2, "a b c", {"a": 1, "b": 1, "c": 1}),
    (3, "a b b a", {"a": 2, "b": 2}),
    (4, "a b c a b", {"a": 2, "b": 2}),
    (5, "b b b b a", {"b": 4}),
    (6, "a", {"a": 1}),
    (7, "a a", {"a": 2}),
    (8, "a b", {"a": 1, "b": 1}),
    (9, "a a a", {"a": 3}),
    (10, "a a b", {"a": 2}),
    (11, "a b a", {"a": 2}),
    (12, "a b b", {"b": 2}),
    (13, "a b c", {"a": 1, "b": 1, "c": 1}),
]

for number, text, expected in witnesses:
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    print(
        f"CLAIM={number:02d} PYTHON_INPUT={text!r} EXPECTED={expected!r} "
        f"CANONICAL={canonical_result!r} CANDIDATE={candidate_result!r}"
    )
    assert canonical_result == expected
    assert candidate_result == expected

print("NOTE: claims 06-13 use synthetic K tokenText values; the displayed")
print("Python strings are an informal join-with-one-space interpretation, not")
print("a theorem connecting tokenText to fixed supplied-semantics strings.")
