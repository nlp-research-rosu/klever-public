#!/usr/bin/env python3
"""Read the entire raw generation log and emit bounded audit-relevant signals."""

from __future__ import annotations

import collections
import hashlib
import pathlib
import re


PATH = pathlib.Path("/generation-evidence/codex-output.log")
SIGNAL = re.compile(
    r"(^exec$|^apply_patch$|^codex$|succeeded in|exited with code|"
    r"\bkompile\b|\bkprove\b|\bkrun\b|#Top|WarnStuckClaimState|"
    r"\[Error\]|RESULT:)"
)

data = PATH.read_bytes()
text = data.decode("utf-8")
lines = text.splitlines()
counts: collections.Counter[str] = collections.Counter()
selected: list[tuple[int, str]] = []

for line_number, line in enumerate(lines, 1):
    if line == "exec":
        counts["exec_headers"] += 1
    if line == "apply_patch":
        counts["apply_patch_headers"] += 1
    if "succeeded in" in line:
        counts["succeeded"] += 1
    if "exited with code" in line:
        counts["nonzero_tool_results"] += 1
    if "#Top" in line:
        counts["top_mentions"] += 1
    if "WarnStuckClaimState" in line:
        counts["stuck_mentions"] += 1
    if "[Error]" in line:
        counts["error_mentions"] += 1
    if SIGNAL.search(line):
        selected.append((line_number, line))

print(f"path={PATH}")
print(f"sha256={hashlib.sha256(data).hexdigest()}")
print(f"bytes={len(data)}")
print(f"lines={len(lines)}")
print(f"signal_counts={dict(sorted(counts.items()))}")
print(f"selected_signal_lines={len(selected)}")
for line_number, line in selected[:500]:
    print(f"{line_number}: {line}")
if len(selected) > 500:
    print(f"... {len(selected) - 500} selected lines omitted")
