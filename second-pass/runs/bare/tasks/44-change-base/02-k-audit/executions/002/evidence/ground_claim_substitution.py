#!/usr/bin/env python3
"""Ground substitutions for the entry claim and its baseString equations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/change-base-audit-20260726")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def base_string_equations(x: int, base: int) -> str:
    if x < base:
        return str(x)
    if base <= x and 0 < base:
        return base_string_equations(x // base, base) + str(x % base)
    raise ValueError("outside verification.k equation coverage")


canonical = load(ROOT / "reference/canonical.py", "ground_canonical")
submitted = load(ROOT / "candidate/solution.py", "ground_submitted")

for x, base in [(8, 3), (0, 2)]:
    precondition = 0 <= x and 2 <= base <= 9
    claimed = base_string_equations(x, base)
    print(
        f"state: X={x}, B={base}, CONT=.K; "
        f"precondition_satisfied={precondition}"
    )
    print(
        f"claimed_result={claimed!r}; submitted_python={submitted(x, base)!r}; "
        f"canonical_python={canonical(x, base)!r}"
    )
