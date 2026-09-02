#!/usr/bin/env python3
"""Ground witnesses for every entry-claim precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
candidate = load(
    Path("/tmp/audit-work/candidate/solution.py"), "candidate_witness"
)

witnesses = [
    ("empty", "", False),
    ("one-alpha", "a", True),
    ("one-nonalpha", "7", False),
    ("long-true", " a", True),
    ("long-last-nonalpha", " !", False),
    ("long-prev-not-space", "aa", False),
]

for claim, text, claimed in witnesses:
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    print(
        f"{claim}: input={text!r} claimed={claimed!r} "
        f"canonical={canonical_result!r} candidate={candidate_result!r}"
    )
    assert canonical_result == claimed
    assert candidate_result == claimed

print(f"satisfying_witnesses={len(witnesses)} all_match=true")
