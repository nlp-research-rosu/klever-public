#!/usr/bin/env python3
"""Render the full structured trace without encrypted reasoning blobs."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-45-16-019f896e-05ca-79e1-bf06-0e03322b8814.jsonl"
)


def redact(value):
    if isinstance(value, dict):
        return {
            key: (
                f"<encrypted blob: {len(item)} characters>"
                if key == "encrypted_content" and isinstance(item, str)
                else redact(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


for line_number, line in enumerate(TRACE.read_text().splitlines(), 1):
    record = json.loads(line)
    print(f"TRACE LINE {line_number}")
    print(json.dumps(redact(record), indent=2, sort_keys=True))
