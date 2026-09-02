#!/usr/bin/env python3
"""Check the completed review's required structure and local evidence links."""

from __future__ import annotations

import re
from pathlib import Path


def main() -> int:
    review = Path("/audit-output/REVIEW.md")
    text = review.read_text()
    expected = "VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n"
    print(
        f"regular_file={review.is_file()} symlink={review.is_symlink()} "
        f"bytes={review.stat().st_size}"
    )
    print(f"exact_verdict_ending={text.endswith(expected)}")
    headings_ok = True
    for stage in range(1, 8):
        present = bool(re.search(rf"^## {stage}\.", text, re.MULTILINE))
        headings_ok = headings_ok and present
        print(f"stage_{stage}_heading={present}")
    links = re.findall(r"\]\((evidence/[^)]+)\)", text)
    missing = [
        link for link in links if not (Path("/audit-output") / link).is_file()
    ]
    print(
        f"evidence_links={len(links)} unique={len(set(links))} "
        f"missing={missing}"
    )
    markers = [
        line
        for line in text.splitlines()
        if line.startswith("VERDICT:") or line.startswith("LEGITIMACY:")
    ]
    print(f"markers={markers}")
    valid = (
        text.endswith(expected)
        and headings_ok
        and not missing
        and len(markers) == 2
    )
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
