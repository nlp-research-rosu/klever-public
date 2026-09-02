#!/usr/bin/env python3
from pathlib import Path
import re


review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
links = re.findall(r"\]\((evidence/[^)]+)\)", text)
missing = [link for link in links if not (review.parent / link).is_file()]
stage_count = len(re.findall(r"^## [1-7]\.", text, re.MULTILINE))
expected_end = "VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n"

print(f"stage_headers={stage_count}")
print(f"evidence_links={len(links)} unique={len(set(links))}")
print(f"missing_links={missing}")
print(f"last_lines={text.splitlines()[-2:]}")
print(f"ends_exact={text.endswith(expected_end)}")

assert stage_count == 7
assert not missing
assert text.endswith(expected_end)
