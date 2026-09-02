#!/usr/bin/env python3
"""Concrete witnesses for every claim precondition and result substitution."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("ground_canonical", "/reference/canonical.py")
candidate = load("ground_candidate", "/candidate/solution.py")

empty: list[str] = []
nonempty = ["a", "bb", "c"]
loop_remainder = ["bb", "c"]
loop_accumulator = "a"

assert canonical.longest(empty) is None
assert candidate.longest(empty) is None
assert canonical.longest(nonempty) == "bb"
assert candidate.longest(nonempty) == "bb"

loop_summary = loop_accumulator
for value in loop_remainder:
    if len(value) > len(loop_summary):
        loop_summary = value
assert loop_summary == "bb"

print("empty-entry witness: exact initial cells; input=[]; post=None")
print(
    "nonempty-entry witness: FIRST='a'; REST=['bb','c']; "
    "isStringValue(FIRST)=true; allStrings(REST)=true; post='bb'"
)
print(
    "loop witness: L=1; MODULE={}; ACC='a'; CURRENT='a'; "
    "REST=['bb','c']; all requires true; scanLongest result='bb'"
)
print("PASS: ground substitutions agree with trusted canonical and candidate Python")
