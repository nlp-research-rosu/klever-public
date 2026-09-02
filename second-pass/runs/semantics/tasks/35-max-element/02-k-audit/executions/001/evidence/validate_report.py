#!/usr/bin/env python3
"""Mechanical final checks for REVIEW.md structure, markers, and local links."""

from __future__ import annotations

import re
from pathlib import Path

REPORT = Path("/audit-output/REVIEW.md")


def main() -> int:
    text = REPORT.read_text(encoding="utf-8")
    problems: list[str] = []

    for stage in range(1, 8):
        if not re.search(rf"^## {stage}\.", text, re.MULTILINE):
            problems.append(f"missing stage {stage}")

    expected_suffix = "VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n"
    if not text.endswith(expected_suffix):
        problems.append("incorrect final marker suffix")
    if text.count("VERDICT:") != 1:
        problems.append(f"VERDICT marker count={text.count('VERDICT:')}")
    if text.count("LEGITIMACY:") != 1:
        problems.append(f"LEGITIMACY marker count={text.count('LEGITIMACY:')}")

    links = sorted(set(re.findall(r"\]\((/audit-output/[^)]+)\)", text)))
    for link in links:
        if not Path(link).exists():
            problems.append(f"missing local link target: {link}")

    evidence_symlinks = [
        str(path) for path in Path("/audit-output/evidence").iterdir() if path.is_symlink()
    ]
    if evidence_symlinks:
        problems.extend(f"unexpected evidence symlink: {path}" for path in evidence_symlinks)

    stages_found = sum(
        bool(re.search(rf"^## {number}\.", text, re.MULTILINE))
        for number in range(1, 8)
    )
    print(f"stages_found={stages_found}")
    print(f"local_links_checked={len(links)}")
    print(f"evidence_symlinks={len(evidence_symlinks)}")
    print(f"problems={len(problems)}")
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
