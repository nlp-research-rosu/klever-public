#!/usr/bin/env python3
"""Render a bounded, reviewer-readable inventory of the full structured trace."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-05-21-019f97a9-e3c3-7762-80df-7fa1b1660ec9.jsonl"
)

for number, line in enumerate(TRACE.open(), 1):
    event = json.loads(line)
    payload = event.get("payload", {})
    event_type = event.get("type")
    payload_type = payload.get("type")
    if event_type == "response_item" and payload_type in {
        "function_call",
        "custom_tool_call",
    }:
        print(
            f"line={number} event={event_type} payload={payload_type} "
            f"name={payload.get('name', '')}"
        )
        data = payload.get("arguments", payload.get("input", ""))
        print(str(data)[:6000])
    elif event_type == "event_msg" and payload_type in {
        "agent_message",
        "task_complete",
        "user_message",
    }:
        print(
            f"line={number} event={event_type} payload={payload_type}"
        )
        print(str(payload.get("message", payload))[:6000])
