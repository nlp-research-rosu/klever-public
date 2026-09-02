#!/usr/bin/env python3
"""Check that the admitted summary is the bridge-free claim verbatim."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/tmp/audit-work/52-below-threshold")


def normalized(lines: list[str], first: str, last_attribute: str) -> str:
    text = "\n".join(lines)
    text = text.replace(first, "DERIVED", 1)
    text = text.replace(last_attribute, "")
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


verification_lines = (ROOT / "verification.k").read_text().splitlines()
spec_lines = (ROOT / "spec.k").read_text().splitlines()

# One-based source ranges: verification.k 55-87, spec.k 8-40.
rule = normalized(
    verification_lines[54:87],
    "  rule",
    "    [priority(40)]",
)
claim = normalized(
    spec_lines[7:40],
    "  claim",
    "    [label(loop-invariant)]",
)

print("base_spec_imports_verification_base=", "imports VERIFICATION-BASE" in "\n".join(spec_lines[:8]))
print("base_spec_imports_summary_module=", "imports VERIFICATION\n" in "\n".join(spec_lines[:43]))
print("normalized_claim_sha256=", hashlib.sha256(claim.encode()).hexdigest())
print("normalized_rule_sha256=", hashlib.sha256(rule.encode()).hexdigest())
print("claim_and_rule_identical=", claim == rule)
if claim != rule:
    raise SystemExit(1)
