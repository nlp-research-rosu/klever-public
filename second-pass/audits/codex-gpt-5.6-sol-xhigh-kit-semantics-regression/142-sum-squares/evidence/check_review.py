#!/usr/bin/env python3
from pathlib import Path
import re

review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
expected = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
if not text.endswith(expected):
    raise SystemExit("review does not end with exact verdict markers")

missing = []
targets = re.findall(r"\]\((evidence/[^)]+)\)", text)
for target in targets:
    path = Path("/audit-output") / target
    if not path.is_file():
        missing.append(target)

print(f"REVIEW_BYTES={review.stat().st_size}")
print(f"EVIDENCE_LINKS={len(targets)}")
print(f"MISSING_LINK_TARGETS={missing}")
print("FINAL_MARKERS=PASS")
raise SystemExit(1 if missing else 0)
