#!/usr/bin/env python3
"""Compare concrete substitutions used in spec-ground.k with both Pythons."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


canonical = load(Path("/reference/canonical.py"), "ground_canonical")
generated = load(
    Path("/tmp/audit-work/7-filter-by-substring/candidate/solution.py"),
    "ground_generated",
)

cases = [
    ([], "a", []),
    (["abc", "xxa", "z"], "a", ["abc", "xxa"]),
]
for strings, substring, formal_postcondition in cases:
    c = canonical(strings, substring)
    g = generated(strings, substring)
    print(
        f"input={strings!r}, substring={substring!r}, "
        f"formal={formal_postcondition!r}, canonical={c!r}, generated={g!r}"
    )
    assert formal_postcondition == c == g

print("ground_substitutions=2 mismatches=0")
