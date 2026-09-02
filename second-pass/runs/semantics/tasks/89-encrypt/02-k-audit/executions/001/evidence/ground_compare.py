#!/usr/bin/env python3
"""Compare concrete substitutions of the formal result with both Pythons."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


canonical = load("/reference/canonical.py", "ground_canonical")
generated = load("/tmp/audit-work/candidate/solution.py", "ground_generated")


def formal_formula(value: str) -> str:
    return "".join(chr((ord(char) - 97 + 4) % 26 + 97) for char in value)


for audit_input in ("", "hi", "A"):
    print(
        f"input={audit_input!r} "
        f"formal={formal_formula(audit_input)!r} "
        f"generated={generated(audit_input)!r} "
        f"canonical={canonical(audit_input)!r}"
    )
