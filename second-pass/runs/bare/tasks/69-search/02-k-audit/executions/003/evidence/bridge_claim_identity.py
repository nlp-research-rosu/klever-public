#!/usr/bin/env python3
"""Mechanical token-level comparison of the loop claim and summary bridge."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def normalized_claim(path: Path) -> str:
    text = path.read_text()
    match = re.search(
        r"claim\s+\[loop-invariant\]\s*:\s*(.*?)\s*endmodule",
        text,
        flags=re.DOTALL,
    )
    assert match is not None
    return " ".join(match.group(1).split())


def normalized_bridge(path: Path) -> str:
    text = path.read_text()
    match = re.search(
        r"rule\s+(.*?)\s*\[priority\(40\)\]\s*endmodule",
        text,
        flags=re.DOTALL,
    )
    assert match is not None
    return " ".join(match.group(1).split())


def main() -> None:
    claim = normalized_claim(
        Path("/tmp/audit-work/candidate-src/loop-lemma-spec.k")
    )
    bridge = normalized_bridge(
        Path("/tmp/audit-work/candidate-src/verification.k")
    )
    print(f"CLAIM_NORMALIZED_SHA256 {hashlib.sha256(claim.encode()).hexdigest()}")
    print(
        f"BRIDGE_NORMALIZED_SHA256 {hashlib.sha256(bridge.encode()).hexdigest()}"
    )
    print(f"TOKEN_LEVEL_IDENTICAL {claim == bridge}")
    print(f"NORMALIZED_TEXT {claim}")
    assert claim == bridge


if __name__ == "__main__":
    main()
