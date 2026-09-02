#!/usr/bin/env python3
"""Exhibit ground witnesses for all three entry-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


root = Path("/tmp/audit-work/reconstruction")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


canonical = load(root / "trusted" / "canonical.py", "canonical_witness")
generated = load(root / "solution.py", "generated_witness")

witnesses = [
    ("balanced_within", [3, 2, 3], 9, True),
    ("unbalanced", [1, 2], 5, False),
    ("balanced_overweight", [3, 2, 3], 1, False),
]

for claim_name, q, w, claimed in witnesses:
    palindrome = q == list(reversed(q))
    within = sum(q) <= w
    if claim_name == "balanced_within":
        precondition = palindrome and within
    elif claim_name == "unbalanced":
        precondition = not palindrome
    else:
        precondition = palindrome and not within
    can = canonical(q, w)
    gen = generated(q, w)
    assert precondition
    assert can is claimed and gen is claimed
    print(
        f"{claim_name}: q={q!r} w={w} "
        f"palindrome={palindrome} sum={sum(q)} "
        f"canonical={can} generated={gen} claimed={claimed}"
    )

print("RESULT: every entry precondition is satisfiable and its ground result agrees")
