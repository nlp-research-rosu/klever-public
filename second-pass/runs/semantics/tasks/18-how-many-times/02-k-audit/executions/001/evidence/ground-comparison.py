#!/usr/bin/env python3
"""Concrete substitution into the entry claim's result expression."""

import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


def independent_overlap_count(string: str, substring: str) -> int:
    return sum(
        string.startswith(substring, i)
        for i in range(len(string) + 1)
    )


canonical = load("/reference/canonical.py", "canonical_ground")
candidate = load("/candidate/solution.py", "candidate_ground")
string = "aaaa"
substring = "aa"
formal_rhs = independent_overlap_count(string, substring)

print(f"input=({string!r}, {substring!r})")
print(f"formal_overlapCount={formal_rhs}")
print(f"canonical={canonical(string, substring)}")
print(f"candidate={candidate(string, substring)}")

assert formal_rhs == canonical(string, substring) == candidate(string, substring) == 3
