#!/usr/bin/env python3
"""Final mechanical consistency check for REVIEW.md."""

from __future__ import annotations

import re
from pathlib import Path


review = Path("/audit-output/REVIEW.md")
text = review.read_text()
expected_end = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
links = re.findall(r"\]\((/audit-output/evidence/[^)]+)\)", text)

checks = {
    "review exists": review.is_file(),
    "exact final pair": text.endswith(expected_end),
    "one verdict line": text.count("VERDICT:") == 1,
    "one legitimacy line": text.count("LEGITIMACY:") == 1,
    "all absolute evidence links resolve": bool(links)
    and all(Path(link).is_file() for link in links),
}
for label, result in checks.items():
    print(f"CHECK {label}: {'PASS' if result else 'FAIL'}")
if not all(checks.values()):
    raise SystemExit(1)
print(f"evidence_link_count={len(links)}")
print("RESULT: PASS")
