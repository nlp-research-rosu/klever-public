#!/usr/bin/env python3
"""Mechanical constructor-level comparison of each claim's executed program."""

from __future__ import annotations

import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/117-select-words-audit")


def normalize(text: str) -> str:
    """Erase whitespace and explicit empty-list unit spellings."""
    return (
        re.sub(r"\s+", "", text)
        .replace(".Strings", "")
        .replace(".Exprs", "")
        .replace(".CmpOps", "")
        .replace(".CompFors", "")
    )


solution = normalize((SCRATCH / "solution.mpy").read_text())
spec = (SCRATCH / "spec.k").read_text()

blocks = re.findall(r"<k>(.*?)=>\s*\.K\s*</k>", spec, flags=re.DOTALL)
print("solution-normalized-chars", len(solution))
print("claim-k-blocks", len(blocks))

failures = 0
for number, block in enumerate(blocks, 1):
    program = normalize(block)
    same = program == solution
    print(
        "claim",
        number,
        "normalized-chars",
        len(program),
        "byte-normalized-equal",
        same,
    )
    if not same:
        mismatch = next(
            (
                index
                for index, pair in enumerate(zip(program, solution))
                if pair[0] != pair[1]
            ),
            min(len(program), len(solution)),
        )
        print("first-mismatch", mismatch)
        print("claim-context", repr(program[max(0, mismatch - 50) : mismatch + 50]))
        print(
            "solution-context",
            repr(solution[max(0, mismatch - 50) : mismatch + 50]),
        )
        failures += 1

raise SystemExit(1 if failures or len(blocks) != 7 else 0)
