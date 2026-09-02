#!/usr/bin/env python3
"""Validate and summarize the untrusted structured generation trace."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def bounded(value: object, limit: int = 3000) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated {len(text) - limit} characters]"


event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls: list[tuple[int, str, str]] = []
messages: list[tuple[int, str, str]] = []
sessions: set[str] = set()
line_total = 0

for trace in sorted(TRACE_ROOT.rglob("*.jsonl")):
    print(f"TRACE_FILE={trace.relative_to(TRACE_ROOT)}")
    with trace.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            line_total += 1
            event = json.loads(line)
            event_type = event.get("type", "<missing>")
            event_types[event_type] += 1
            payload = event.get("payload", {})
            payload_type = payload.get("type", "<missing>")
            payload_types[f"{event_type}/{payload_type}"] += 1
            if event_type == "session_meta":
                session = payload.get("session_id")
                if isinstance(session, str):
                    sessions.add(session)
            if event_type == "response_item":
                if payload_type in {"custom_tool_call", "function_call"}:
                    tool_calls.append(
                        (
                            line_number,
                            str(payload.get("name")),
                            bounded(payload.get("input", "")),
                        )
                    )
                elif payload_type == "message":
                    role = str(payload.get("role"))
                    if role in {"assistant", "developer", "user"}:
                        messages.append(
                            (
                                line_number,
                                role,
                                bounded(payload.get("content", ""), 2000),
                            )
                        )
            if event_type == "event_msg" and payload_type in {
                "agent_message",
                "task_complete",
            }:
                messages.append(
                    (
                        line_number,
                        payload_type,
                        bounded(payload.get("message") or payload.get("last_agent_message"), 2000),
                    )
                )

print(f"JSONL_LINE_COUNT={line_total}")
print(f"SESSION_IDS={sorted(sessions)}")
print("EVENT_TYPE_COUNTS")
for key, count in sorted(event_types.items()):
    print(f"  {key}: {count}")
print("PAYLOAD_TYPE_COUNTS")
for key, count in sorted(payload_types.items()):
    print(f"  {key}: {count}")
print(f"TOOL_CALL_COUNT={len(tool_calls)}")
for line_number, name, tool_input in tool_calls:
    print(f"TOOL_CALL line={line_number} name={name}\n{tool_input}")
print(f"MESSAGE_COUNT={len(messages)}")
for line_number, role, content in messages:
    print(f"MESSAGE line={line_number} role={role}\n{content}")
