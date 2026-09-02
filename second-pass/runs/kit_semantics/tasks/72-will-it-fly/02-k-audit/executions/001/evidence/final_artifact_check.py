#!/usr/bin/env python3
"""Check the reviewer report's terminal markers and local evidence links."""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path


review = Path("/audit-output/REVIEW.md")
text = review.read_text()
lines = text.splitlines()
assert lines[-2:] == [
    "VERDICT: CONCERNS",
    "LEGITIMACY: LEGIT",
]

targets = re.findall(r"\]\((/[^)]+)\)", text)
checked: set[Path] = set()
for target in targets:
    path_text = target
    if re.search(r":\d+$", path_text):
        path_text = path_text.rsplit(":", 1)[0]
    path = Path(path_text)
    assert path.exists(), f"missing report link: {target}"
    checked.add(path)

evidence_root = Path("/audit-output/evidence")
regular_files = 0
for path in evidence_root.iterdir():
    mode = os.lstat(path).st_mode
    assert not stat.S_ISLNK(mode), f"symlinked evidence entry: {path}"
    if stat.S_ISREG(mode):
        regular_files += 1

print("terminal_markers_exact=true")
print(f"local_report_links_checked={len(checked)}")
print(f"direct_regular_evidence_files={regular_files}")
print("FINAL_ARTIFACT_CHECK=PASS")
