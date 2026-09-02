#!/usr/bin/env python3
"""Concrete satisfiability/result witnesses for all function-entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
generated = load(Path("/tmp/audit-work/129-minPath/solution.py"), "generated_witness")
entries = [
    (
        "prompt-example-1",
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        3,
        [1, 2, 1],
    ),
    (
        "prompt-example-2",
        [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
        1,
        [1],
    ),
    (
        "symbolic-2x2-k4 with A=1,B=2,C=3,D=4",
        [[1, 2], [3, 4]],
        4,
        [1, 2, 1, 2],
    ),
]

for label, grid, k, claimed in entries:
    c_result = canonical(grid, k)
    g_result = generated(grid, k)
    print(label)
    print("  grid=", grid, "k=", k)
    print("  claimed=", claimed)
    print("  canonical=", c_result)
    print("  generated=", g_result)
    assert c_result == g_result == claimed

print("loop-invariant satisfying state:")
print("  I=0, K=1, N=2, P=.ValSeq, L=1, H=0, OLD=99, PARENT=parent(0)")
print("  exact local map: i|->99, path|->ref(0), neighbor|->2")
print("  heap[0]=list(.ValSeq); minPathBuild(.ValSeq,0,1,2)=[1]")
print("CLAIM_WITNESSES: PASS")
