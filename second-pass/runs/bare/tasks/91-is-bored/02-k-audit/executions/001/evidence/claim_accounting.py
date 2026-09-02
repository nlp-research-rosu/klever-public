#!/usr/bin/env python3
"""Concrete witnesses for every submitted entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


canonical = load_entry("trusted_claim_oracle", Path("/reference/canonical.py"))
submitted = load_entry(
    "submitted_claim_subject",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)

claims = [
    (1, "Hello world", 0),
    (2, "The sky is blue. The sun is shining. I love this weather", 1),
    (3, "I am bored. I am still bored! Are you? I think so.", 3),
    (4, " I am here?You are there!  I agree", 2),
    (5, "It is cold. Island life! In time? I agree", 1),
    (6, "... ! ?  . I count!", 1),
    (7, "\tI tabbed.\nI newline?\rNot me!", 2),
    # boredSpec("I first! No. I second?") reduces to 2.
    (8, "I first! No. I second?", 2),
]

submitted_disagreements = 0
canonical_disagreements = 0
for number, text, claimed in claims:
    got_submitted = submitted(text)
    got_canonical = canonical(text)
    print(
        f"claim={number} satisfying_initial_state="
        f"<k>start</k> <program>solutionModule</program> "
        f"<input>{text!r}</input> <result>0</result>"
    )
    print(
        f"claim={number} claimed_final={claimed} "
        f"submitted_python={got_submitted} canonical_python={got_canonical}"
    )
    submitted_disagreements += got_submitted != claimed
    canonical_disagreements += got_canonical != claimed

print(f"claim_count={len(claims)}")
print(f"claimed_vs_submitted_mismatch_count={submitted_disagreements}")
print(f"claimed_vs_canonical_mismatch_count={canonical_disagreements}")
raise SystemExit(1 if submitted_disagreements else 0)
