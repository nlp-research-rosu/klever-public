#!/usr/bin/env python3
"""Mechanical handoff checks for REVIEW.md."""

from __future__ import annotations

import re
from pathlib import Path


def main() -> int:
    review_path = Path("/audit-output/REVIEW.md")
    text = review_path.read_text()
    lines = text.splitlines()
    expected_headings = [
        "## 1. Input and provenance integrity",
        "## 2. Program fidelity and candidate-versus-canonical checks",
        "## 3. Clean proof reconstruction",
        "## 4. Adequacy and real-program pinning",
        "## 5. Rule-by-rule static soundness review",
        "## 6. Fresh non-vacuity test",
        "## 7. Proven versus assumed accounting",
    ]
    positions = [lines.index(heading) for heading in expected_headings]
    final_ok = lines[-2:] == [
        "VERDICT: FAIL",
        "LEGITIMACY: NOT_LEGIT",
    ]
    references = sorted(set(re.findall(r"`(evidence/[^`]+)`", text)))
    missing = [
        reference
        for reference in references
        if not (Path("/audit-output") / reference).exists()
    ]
    print(f"seven_stages_in_order={positions == sorted(positions)}")
    print(f"final_markers_exact={final_ok}")
    print(f"evidence_references={len(references)}")
    print(f"missing_evidence_references={missing}")
    print(f"review_bytes={review_path.stat().st_size}")
    return int(positions != sorted(positions) or not final_ok or bool(missing))


if __name__ == "__main__":
    raise SystemExit(main())
