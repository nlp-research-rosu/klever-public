#!/usr/bin/env python3
"""Read the complete generation trace and emit a bounded audit-oriented digest."""

from __future__ import annotations

import json
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
interesting_words = (
    "kompile",
    "kprove",
    "krun",
    "solution",
    "semantic.k",
    "verification.k",
    "spec.k",
    "apply_patch",
    "exec_command",
    "#Top",
    "WarnStuck",
    "error",
    "failed",
)


def flatten_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for child in value:
            yield from flatten_strings(child)
    elif isinstance(value, dict):
        for child in value.values():
            yield from flatten_strings(child)


print(f"TRACE={trace}")
with trace.open() as stream:
    for line_number, line in enumerate(stream, 1):
        item = json.loads(line)
        strings = list(flatten_strings(item))
        joined = "\n".join(strings)
        if any(word.lower() in joined.lower() for word in interesting_words):
            compact = " | ".join(part.replace("\n", "\\n") for part in strings)
            print(f"{line_number}: {compact[:5000]}")

log = Path("/generation-evidence/codex-output.log")
print(f"CODEX_OUTPUT={log}")
with log.open(errors="replace") as stream:
    for line_number, line in enumerate(stream, 1):
        if any(word.lower() in line.lower() for word in interesting_words):
            print(f"{line_number}: {line.rstrip()[:5000]}")
