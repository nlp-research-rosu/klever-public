#!/usr/bin/env python3
"""Mechanical token-level comparison of the claimed and submitted program terms."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
submitted = (ROOT / "regenerated-solution.mpy").read_text(encoding="utf-8")
verification = (ROOT / "verification.k").read_text(encoding="utf-8")


def rule_rhs(source: str, lhs: str, end_marker: str) -> str:
    pattern = (
        rf"rule\s+{re.escape(lhs)}\s*=>\s*(.*?)"
        rf"(?=\n\s*{re.escape(end_marker)})"
    )
    match = re.search(pattern, source, flags=re.DOTALL)
    assert match is not None, f"could not extract rule for {lhs}"
    return match.group(1)


body = rule_rhs(verification, "multiplyBody", "syntax Program")
program = rule_rhs(verification, "multiplyProgram", "// Mathematical")
expanded_program = program.replace("multiplyBody", body)


def normalize_constructor_term(source: str) -> str:
    without_comments = re.sub(r"//[^\n]*", "", source)
    without_empty_list_names = without_comments.replace(".Stmts", "")
    return re.sub(r"\s+", "", without_empty_list_names)


submitted_normal = normalize_constructor_term(submitted)
claimed_normal = normalize_constructor_term(expanded_program)
submitted_sha = hashlib.sha256(submitted_normal.encode()).hexdigest()
claimed_sha = hashlib.sha256(claimed_normal.encode()).hexdigest()

print("COMPARISON: trusted-regenerated solution.mpy vs verification.k")
print("NORMALIZATION: remove comments/whitespace and explicit .Stmts empties")
print("CLAIM_EXPANSION: multiplyProgram RHS with multiplyBody RHS substituted")
print(f"SUBMITTED_NORMALIZED_SHA256: {submitted_sha}")
print(f"CLAIMED_NORMALIZED_SHA256: {claimed_sha}")
print(f"NORMALIZED_BYTE_LENGTH: {len(submitted_normal.encode())}")
if submitted_normal != claimed_normal:
    print("SUBMITTED_NORMALIZED:", submitted_normal)
    print("CLAIMED_NORMALIZED:", claimed_normal)
    raise SystemExit(1)
print("CONSTRUCTOR_LEVEL_PROGRAM_IDENTITY: PASS")
