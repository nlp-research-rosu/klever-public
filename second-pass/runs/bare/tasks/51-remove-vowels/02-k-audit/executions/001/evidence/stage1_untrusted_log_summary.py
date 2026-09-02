#!/usr/bin/env python3
"""Read the complete untrusted text log and emit bounded provenance facts."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


path = Path("/candidate/codex-output.log")
data = path.read_bytes()
text = data.decode("utf-8", errors="replace")
lines = text.splitlines()
patterns = {
    "kprove": re.compile(r"kprove", re.I),
    "kompile": re.compile(r"kompile", re.I),
    "krun": re.compile(r"\bkrun\b", re.I),
    "top": re.compile(r"#Top"),
    "error": re.compile(r"\b(error|failed|failure)\b", re.I),
    "result_claim": re.compile(r"KPROVE_PASSED|RESULT:", re.I),
}
counts: collections.Counter[str] = collections.Counter()
selected: list[str] = []
for line_no, line in enumerate(lines, 1):
    matched = []
    for label, pattern in patterns.items():
        if pattern.search(line):
            counts[label] += 1
            matched.append(label)
    if matched and len(selected) < 80:
        selected.append(
            f"{line_no} [{','.join(matched)}] {line[:500]}"
        )

print(f"path={path}")
print(f"bytes={len(data)} lines={len(lines)} sha256={hashlib.sha256(data).hexdigest()}")
print(f"pattern_counts={dict(counts)}")
print("selected_lines_begin")
for line in selected:
    print(line)
print("selected_lines_end")
