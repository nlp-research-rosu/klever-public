#!/usr/bin/env python3
"""Mechanical final checks for REVIEW.md structure and evidence links."""

from __future__ import annotations

import re
from pathlib import Path


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/validate_review.py")
    review = Path("/audit-output/REVIEW.md")
    text = review.read_text()
    lines = text.splitlines()
    headings = re.findall(r"^## ([1-7])\. ", text, flags=re.MULTILINE)
    assert headings == [str(number) for number in range(1, 8)], headings
    assert lines[-2:] == [
        "VERDICT: FAIL",
        "LEGITIMACY: NOT_LEGIT",
    ]
    links = re.findall(r"\]\((evidence/[^)]+)\)", text)
    missing = [
        relative
        for relative in links
        if not (Path("/audit-output") / relative).is_file()
    ]
    assert not missing, missing
    print(f"SEVEN_ORDERED_STAGES: {headings}")
    print(f"EVIDENCE_LINKS_CHECKED: {len(links)}")
    print("FINAL_LINES: VERDICT: FAIL | LEGITIMACY: NOT_LEGIT")
    print("REVIEW_VALIDATION: PASS")


if __name__ == "__main__":
    main()
