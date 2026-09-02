#!/usr/bin/env python3
"""Inspect every structured generation-trace event and summarize untrusted claims."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
files = sorted(root.rglob("*.jsonl"))
assert files

event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls = []
agent_messages = []
sessions = []
task_completions = []
event_count = 0

for path in files:
    for line_number, line in enumerate(path.open(), 1):
        event = json.loads(line)
        event_count += 1
        event_types[str(event.get("type"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if event.get("type") == "session_meta":
                sessions.append(
                    {
                        "file": str(path),
                        "line": line_number,
                        "session_id": payload.get("session_id"),
                        "cwd": payload.get("cwd"),
                        "cli_version": payload.get("cli_version"),
                        "model_provider": payload.get("model_provider"),
                    }
                )
            if payload_type in {"custom_tool_call", "function_call"}:
                call_input = payload.get("input") or payload.get("arguments") or ""
                if not isinstance(call_input, str):
                    call_input = json.dumps(call_input, sort_keys=True)
                tool_calls.append(
                    {
                        "file": str(path),
                        "line": line_number,
                        "name": payload.get("name"),
                        "input_sha256": hashlib.sha256(call_input.encode()).hexdigest(),
                        "input_prefix": call_input[:300],
                    }
                )
            if payload_type == "agent_message":
                agent_messages.append(
                    {
                        "file": str(path),
                        "line": line_number,
                        "phase": payload.get("phase"),
                        "message": payload.get("message"),
                    }
                )
            if payload_type == "task_complete":
                task_completions.append(
                    {
                        "file": str(path),
                        "line": line_number,
                        "payload": payload,
                    }
                )

summary = {
    "trace_files": [str(path) for path in files],
    "event_count": event_count,
    "event_types": dict(sorted(event_types.items())),
    "payload_types": dict(sorted(payload_types.items())),
    "sessions": sessions,
    "tool_call_count": len(tool_calls),
    "tool_calls": tool_calls,
    "agent_messages": agent_messages,
    "task_completions": task_completions,
}
print(json.dumps(summary, ensure_ascii=True, indent=2))
