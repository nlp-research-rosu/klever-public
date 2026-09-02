#!/usr/bin/env python3
from pathlib import Path
import re

review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
lines = text.splitlines()
assert lines[-2:] == ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
assert text.count("VERDICT: ") == 1
assert text.count("LEGITIMACY: ") == 1

missing = []
for target in re.findall(r"\]\((evidence/[^)]+)\)", text):
    if not (Path("/audit-output") / target).is_file():
        missing.append(target)
assert not missing, missing

for stage in range(1, 8):
    assert re.search(rf"^## {stage}\.", text, flags=re.MULTILINE), stage

evidence_link_count = len(re.findall(r"\]\(evidence/[^)]+\)", text))
print(f"review_bytes={len(text.encode('utf-8'))}")
print(f"evidence_links={evidence_link_count}")
print("seven_stages=present")
print("terminal_markers=exact")
print("RESULT: PASS")
