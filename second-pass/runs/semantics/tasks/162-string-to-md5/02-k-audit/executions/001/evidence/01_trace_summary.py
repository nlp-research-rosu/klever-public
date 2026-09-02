#!/usr/bin/env python3
"""Render every structured generation event in a compact audit-friendly form."""

import json
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/26/"
    "rollout-2026-07-26T03-06-58-019f9d76-85b8-79c2-bb46-5f4061c8d390.jsonl"
)


def clipped(value, limit=5000):
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[clipped {len(text) - limit} chars]..."


for number, raw in enumerate(TRACE.read_text().splitlines(), 1):
    event = json.loads(raw)
    payload = event.get("payload", {})
    event_type = event.get("type")
    payload_type = payload.get("type") if isinstance(payload, dict) else None
    print(f"LINE {number} EVENT {event_type} PAYLOAD {payload_type}")
    if event_type == "response_item":
        if payload_type in {"function_call", "custom_tool_call"}:
            print("NAME", payload.get("name"))
            print(clipped(payload.get("arguments", payload.get("input", "")), 12000))
        elif payload_type == "function_call_output":
            print(clipped(payload.get("output", ""), 5000))
        elif payload_type == "custom_tool_call_output":
            print(clipped(payload.get("output", ""), 5000))
        elif payload_type == "message":
            print(clipped(payload.get("content", ""), 12000))
        elif payload_type == "reasoning":
            summary = payload.get("summary", [])
            print(clipped(summary, 12000))
    elif event_type == "event_msg" and payload_type in {
        "agent_message",
        "user_message",
        "task_complete",
    }:
        print(clipped(payload, 12000))
