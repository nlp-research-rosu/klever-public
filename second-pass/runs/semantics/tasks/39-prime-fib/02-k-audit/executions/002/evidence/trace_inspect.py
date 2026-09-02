#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize its shape."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

trace_root = Path("/generation-evidence/codex-trace")
files = sorted(trace_root.rglob("*"))
trace_files = [path for path in files if path.is_file()]
print(f"trace files={len(trace_files)}")

for path in trace_files:
    counts: Counter[str] = Counter()
    parse_errors = 0
    lines = 0
    first_timestamp = None
    last_timestamp = None
    tool_names: Counter[str] = Counter()
    assistant_messages = 0
    for raw in path.read_text(errors="replace").splitlines():
        lines += 1
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            parse_errors += 1
            continue
        event_type = str(obj.get("type", "<missing>"))
        counts[event_type] += 1
        timestamp = obj.get("timestamp")
        if timestamp is not None:
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
        payload = obj.get("payload")
        if isinstance(payload, dict):
            payload_type = payload.get("type")
            if payload_type is not None:
                counts[f"payload:{payload_type}"] += 1
            if payload_type == "function_call":
                tool_names[str(payload.get("name", "<missing>"))] += 1
            if payload_type == "message" and payload.get("role") == "assistant":
                assistant_messages += 1
    print(f"file={path}")
    print(
        f"lines={lines} parse_errors={parse_errors} "
        f"first_timestamp={first_timestamp} last_timestamp={last_timestamp}"
    )
    print(f"event_counts={dict(sorted(counts.items()))}")
    print(f"tool_counts={dict(sorted(tool_names.items()))}")
    print(f"assistant_messages={assistant_messages}")
