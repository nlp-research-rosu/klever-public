#!/usr/bin/env python3
"""Ground witness showing that the fresh postcondition mutation is false."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens


value = "(()(())((())))"
canonical = load(Path("/tmp/audit-work/reference/canonical.py"), "canonical_mutation")
submitted = load(Path("/tmp/audit-work/candidate/solution.py"), "submitted_mutation")
canonical_result = canonical(value)
submitted_result = submitted(value)
print(
    f"input={value!r} canonical={canonical_result!r} "
    f"submitted={submitted_result!r} mutated_required=[5]"
)
assert canonical_result == [4]
assert submitted_result == [4]
print("FALSE_POSTCONDITION_WITNESS=PASS")
