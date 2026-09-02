#!/usr/bin/env python3
"""Final structural validation of REVIEW.md and its evidence links."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def main() -> int:
    review = Path("/audit-output/REVIEW.md")
    text = review.read_text(encoding="utf-8")
    lines = text.splitlines()
    expected_tail = ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
    links = re.findall(r"\]\((evidence/[^)]+)\)", text)
    missing = [target for target in links if not (review.parent / target).is_file()]
    evidence_files = sorted(
        path for path in (review.parent / "evidence").iterdir() if path.is_file()
    )

    print(f"REVIEW_SHA256={hashlib.sha256(review.read_bytes()).hexdigest()}")
    print(f"LAST_TWO_LINES={lines[-2:]!r}")
    print(f"TAIL_VALID={lines[-2:] == expected_tail}")
    print(f"EVIDENCE_LINK_COUNT={len(links)}")
    print(f"MISSING_LINKS={missing!r}")
    print(f"EVIDENCE_FILE_COUNT={len(evidence_files)}")
    return 0 if lines[-2:] == expected_tail and not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
