#!/usr/bin/env python3
"""Exhibit concrete states/inputs satisfying both candidate entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_max


canonical = load(Path("/reference/canonical.py"), "witness_canonical")
generated = load(Path("/tmp/audit-work/repro/solution.py"), "witness_generated")

words = ["ba", "ab"]
print("COMMAND: python3 /audit-output/evidence/ground_witness.py")
print("contract witness WordSeq = wCons(codes('ba'), wCons(codes('ab'), .WordSeq))")
print("loop witness: iterator is that WordSeq; BEST=''; SCORE=0;")
print("loop scope 1 has words=['ba','ab'], best='', max_unique=0, word='', unique=0")
print(f"canonical({words!r})={canonical(words)!r}")
print(f"generated({words!r})={generated(words)!r}")
print("claimed summary bestWord='ab'; bestScore=2")
assert canonical(words) == generated(words) == "ab"
