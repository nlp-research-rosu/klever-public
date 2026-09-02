#!/usr/bin/env python3
"""Final structural validation of REVIEW.md and its evidence links."""

from __future__ import annotations

import re
from pathlib import Path


REVIEW = Path("/audit-output/REVIEW.md")


def main() -> int:
    text = REVIEW.read_text()
    lines = text.splitlines()
    failures: list[str] = []
    expected_tail = ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
    if lines[-2:] != expected_tail:
        failures.append(f"bad verdict tail: {lines[-2:]!r}")
    if text.count("VERDICT:") != 1:
        failures.append(f"VERDICT count is {text.count('VERDICT:')}")
    if text.count("LEGITIMACY:") != 1:
        failures.append(
            f"LEGITIMACY count is {text.count('LEGITIMACY:')}"
        )
    for stage in range(1, 8):
        if f"## {stage}." not in text:
            failures.append(f"missing stage heading {stage}")
    links = re.findall(r"\]\((evidence/[^)]+)\)", text)
    missing = [
        link for link in links if not (REVIEW.parent / link).is_file()
    ]
    failures.extend(f"missing evidence link {link}" for link in missing)
    print(f"review_bytes={len(text.encode())}")
    print(f"review_lines={len(lines)}")
    print(f"evidence_links={len(links)}")
    print(f"missing_evidence_links={len(missing)}")
    print(f"tail={lines[-2:]!r}")
    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
