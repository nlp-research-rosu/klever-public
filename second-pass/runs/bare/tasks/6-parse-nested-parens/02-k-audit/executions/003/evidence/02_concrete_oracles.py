#!/usr/bin/env python3
"""Oracle outputs for the exact concrete K inputs used in Stage 3."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens


canonical = load(Path("/tmp/audit-work/reference/canonical.py"), "canonical_stage3")
submitted = load(Path("/tmp/audit-work/candidate/solution.py"), "submitted_stage3")

for value in (
    "(()()) ((())) () ((())()())",
    "()()",
    "",
    "()  (())",
):
    print(
        f"input={value!r} canonical={canonical(value)!r} "
        f"submitted={submitted(value)!r}"
    )
