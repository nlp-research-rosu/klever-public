#!/usr/bin/env python3
"""Ground satisfying witnesses for all eleven entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "canonical_witness")
candidate = load(Path("/tmp/audit-work/candidate/solution.py"), "candidate_witness")

witnesses = [
    # claim, satisfying substitution, concrete source string, claimed result
    (1, "N=7,D=2 (D>0)", "3.5", 4),
    (2, "I=2 (I>=0)", "2.5", 3),
    (3, "I=2 (I>=0)", "-2.5", -3),
    (4, "I=2 (I>=0)", "2.25", 2),
    (5, "I=2 (I>=0)", "2.75", 3),
    (6, "I=2 (I>=0)", "-2.25", -2),
    (7, "I=2 (I>=0)", "-2.75", -3),
    (8, "ground precondition", "10", 10),
    (9, "ground precondition", "15.3", 15),
    (10, "ground precondition", "14.5", 15),
    (11, "ground precondition", "-14.5", -15),
]

failures = 0
for claim, substitution, text, formal_result in witnesses:
    candidate_result = candidate(text)
    canonical_result = canonical(text)
    ok = candidate_result == canonical_result == formal_result
    failures += int(not ok)
    print(
        f"claim={claim} substitution={substitution!r} input={text!r} "
        f"formal={formal_result} candidate={candidate_result} "
        f"canonical={canonical_result} status={'OK' if ok else 'MISMATCH'}"
    )

print(f"claims={len(witnesses)} failures={failures}")
raise SystemExit(1 if failures else 0)
