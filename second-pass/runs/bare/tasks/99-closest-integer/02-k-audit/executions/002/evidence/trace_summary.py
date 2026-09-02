#!/usr/bin/env python3
"""Summarize every JSONL event in the untrusted structured generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
files = sorted(root.rglob("*.jsonl"))
assert files, "no structured trace"

for path in files:
    counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    tool_calls: list[tuple[int, str]] = []
    tool_outputs = 0
    parse_errors: list[int] = []
    first_timestamp = None
    last_timestamp = None
    final_messages: list[str] = []
    lines = 0
    with path.open() as stream:
        for lines, raw in enumerate(stream, 1):
            try:
                event = json.loads(raw)
            except json.JSONDecodeError:
                parse_errors.append(lines)
                continue
            kind = str(event.get("type"))
            counts[kind] += 1
            timestamp = event.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            payload = event.get("payload", {})
            payload_kind = str(payload.get("type"))
            payload_counts[payload_kind] += 1
            if payload_kind in {"custom_tool_call", "function_call"}:
                name = payload.get("name", "")
                call_input = payload.get("input", payload.get("arguments", ""))
                tool_calls.append((lines, f"{name}: {call_input}"))
            if payload_kind in {"custom_tool_call_output", "function_call_output"}:
                tool_outputs += 1
            if payload_kind in {"agent_message", "message"}:
                text = payload.get("message", "")
                if text:
                    final_messages.append(text)

    print(f"TRACE {path}")
    print(f"lines={lines} first={first_timestamp} last={last_timestamp}")
    print(f"event_types={dict(sorted(counts.items()))}")
    print(f"payload_types={dict(sorted(payload_counts.items()))}")
    print(f"tool_calls={len(tool_calls)} tool_outputs={tool_outputs} parse_errors={parse_errors}")
    for line, call in tool_calls:
        compact = call.replace("\n", "\\n")
        print(f"CALL line={line} {compact[:1000]}")
    for message in final_messages:
        print(f"FINAL {message[:2000]}")
