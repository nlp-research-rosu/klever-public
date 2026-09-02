#!/usr/bin/env python3
"""Confirm that the promoted loop rule has the proved claim's exact contract."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/133-sum-squares-audit")


def normalize(block: str) -> str:
    block = re.sub(r"^\s*claim\s+\[loop-correct\]\s*:\s*", "", block)
    block = re.sub(r"^\s*rule\s*", "", block)
    block = re.sub(r"\s*\[priority\(40\)\]\s*$", "", block)
    return re.sub(r"\s+", " ", block).strip()


def main() -> int:
    spec = (ROOT / "spec.k").read_text()
    verification = (ROOT / "verification.k").read_text()
    claim_match = re.search(
        r"claim\s+\[loop-correct\]\s*:(.*?requires\s+notBool\s+\(L\s+in_keys\(GLOBAL\)\))",
        spec,
        flags=re.S,
    )
    rule_match = re.search(
        r"\n\s*rule\s*(<k>.*?requires\s+notBool\s+\(L\s+in_keys\(GLOBAL\)\)\s*"
        r"\[priority\(40\)\])",
        verification,
        flags=re.S,
    )
    if claim_match is None or rule_match is None:
        print("extraction_failed")
        return 2
    claim = normalize("claim [loop-correct]:" + claim_match.group(1))
    rule = normalize("rule " + rule_match.group(1))
    print(f"claim_sha256={hashlib.sha256(claim.encode()).hexdigest()}")
    print(f"rule_sha256={hashlib.sha256(rule.encode()).hexdigest()}")
    print(f"normalized_text_identical={claim == rule}")
    print("promoted_extra_attribute=priority(40)")
    return 0 if claim == rule else 1


if __name__ == "__main__":
    raise SystemExit(main())
