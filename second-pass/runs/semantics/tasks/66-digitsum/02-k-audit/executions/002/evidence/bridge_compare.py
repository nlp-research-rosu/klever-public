#!/usr/bin/env python3
"""Check that proof-local operational bridges are exact copies of proved claims."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


SPEC = Path("/candidate/spec.k").read_text()
VERIFICATION = Path("/candidate/verification.k").read_text()


def extract(text: str, pattern: str, following: str) -> str:
    match = re.search(pattern + r"(.*?)" + following, text, re.S)
    if match is None:
        raise RuntimeError(f"could not extract {pattern!r}")
    return match.group(1)


def normalize(body: str) -> str:
    body = re.sub(r"//.*$", "", body, flags=re.M)
    body = re.sub(r"\[priority\(20\)\]\s*$", "", body)
    return re.sub(r"\s+", " ", body).strip()


pairs = [
    (
        "initialization",
        extract(
            SPEC,
            r"claim\s+\[initialization\]\s*:",
            r"\nendmodule",
        ),
        extract(
            VERIFICATION,
            r"rule\s+\[digit-sum-initialization-lemma\]\s*:",
            r"\n\s*rule\s+\[digit-sum-loop-lemma\]",
        ),
    ),
    (
        "loop",
        extract(
            SPEC,
            r"claim\s+\[loop-invariant\]\s*:",
            r"\nendmodule",
        ),
        extract(
            VERIFICATION,
            r"rule\s+\[digit-sum-loop-lemma\]\s*:",
            r"\nendmodule",
        ),
    ),
]

print("COMMAND: python3 /audit-output/evidence/bridge_compare.py")
all_equal = True
for name, claim, bridge in pairs:
    normalized_claim = normalize(claim)
    normalized_bridge = normalize(bridge)
    equal = normalized_claim == normalized_bridge
    all_equal &= equal
    print(
        f"{name}: exact_context_equal={equal} "
        f"claim_sha256={hashlib.sha256(normalized_claim.encode()).hexdigest()} "
        f"bridge_sha256={hashlib.sha256(normalized_bridge.encode()).hexdigest()}"
    )
print(f"ALL_BRIDGES_EXACT={all_equal}")
print(f"EXIT_STATUS={0 if all_equal else 1}")
raise SystemExit(0 if all_equal else 1)
