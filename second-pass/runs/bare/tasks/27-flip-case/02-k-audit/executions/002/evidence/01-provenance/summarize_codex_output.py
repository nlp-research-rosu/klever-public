#!/usr/bin/env python3
"""Scan every line of the untrusted flat Codex output and report bounded facts."""

from __future__ import annotations

import collections
from pathlib import Path


PATH = Path("/generation-evidence/codex-output.log")
needles = (
    "#Top",
    "EXIT=",
    "RESULT:",
    "kprove ",
    "kompile ",
    "krun ",
    "apply_patch",
    "semantic.k",
    "verification.k",
    "spec.k",
    "unicode-case.k",
)
counts = collections.Counter()
selected = []
line_count = 0
decode_errors = 0
with PATH.open("rb") as stream:
    for line_count, raw in enumerate(stream, 1):
        text = raw.decode("utf-8", "replace").rstrip("\n")
        decode_errors += text.count("\ufffd")
        matched = [needle for needle in needles if needle in text]
        for needle in matched:
            counts[needle] += 1
        if matched and len(selected) < 120:
            selected.append((line_count, matched, text[:500]))

print("path", PATH)
print("line_count", line_count)
print("replacement_character_count", decode_errors)
print("needle_counts", dict(counts))
print("selected_line_count", len(selected))
for line_number, matched, text in selected:
    print("line", line_number, "matched", matched, "text", repr(text))
