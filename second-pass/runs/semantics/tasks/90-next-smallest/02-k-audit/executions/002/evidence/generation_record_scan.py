#!/usr/bin/env python3
"""Bounded structural scan of the complete untrusted generation record set."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_records:
    document = json.loads(path.read_text())
    print(
        f"JSON {path}: type={type(document).__name__} "
        f"keys={sorted(document) if isinstance(document, dict) else 'n/a'}"
    )

for path in [
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]:
    text = path.read_text(errors="replace")
    print(
        f"TEXT {path}: bytes={len(text.encode())} lines={len(text.splitlines())} "
        f"top_count={text.count('#Top')} "
        f"passed_marker_count={text.count('KPROVE_PASSED')}"
    )

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
for path in trace_files:
    outer = Counter()
    payload = Counter()
    count = 0
    first_timestamp = None
    last_timestamp = None
    for count, line in enumerate(path.open(), 1):
        event = json.loads(line)
        first_timestamp = first_timestamp or event.get("timestamp")
        last_timestamp = event.get("timestamp")
        outer[event.get("type", "<none>")] += 1
        inner = event.get("payload")
        if isinstance(inner, dict):
            payload[inner.get("type", "<none>")] += 1
    print(
        f"TRACE {path}: events={count} first={first_timestamp} last={last_timestamp} "
        f"outer={dict(outer)} payload={dict(payload)}"
    )
