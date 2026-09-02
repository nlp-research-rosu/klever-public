#!/usr/bin/env python3
"""Mechanical completeness checks for the final audit report."""

from __future__ import annotations

import re
from pathlib import Path

REVIEW = Path("/audit-output/REVIEW.md")


def main() -> None:
    text = REVIEW.read_text()
    lines = text.splitlines()
    assert lines[-2:] == ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
    for stage in range(1, 8):
        assert re.search(rf"^## {stage}\.", text, re.MULTILINE), stage

    missing: list[str] = []
    evidence_links = sorted(
        {
            match
            for match in re.findall(r"\]\((evidence/[^)]+)\)", text)
            if not match.startswith(("http:", "https:"))
        }
    )
    for relative in evidence_links:
        if not (REVIEW.parent / relative).exists():
            missing.append(relative)
    assert not missing, missing

    print(f"review={REVIEW}")
    print("stage_count=7")
    print(f"evidence_link_count={len(evidence_links)}")
    print("missing_evidence_links=0")
    print("terminal_markers=VALID")
    print("REVIEW_VALIDATION=PASS")


if __name__ == "__main__":
    main()
