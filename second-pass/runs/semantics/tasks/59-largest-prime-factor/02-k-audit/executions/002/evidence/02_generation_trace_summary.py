#!/usr/bin/env python3
"""Bounded, reviewer-authored extraction of every structured generation event."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T00-38-25-019f8d7b-710f-7f03-8454-aa05bfcdc438.jsonl"
)


def bounded(value: object, limit: int = 1800) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, sort_keys=True)
    text = text.replace("\x1b", "<ESC>")
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + f"\n... <{len(text) - limit} chars omitted> ...\n" + text[-half:]


for line_number, line in enumerate(TRACE.open(), 1):
    event = json.loads(line)
    kind = event.get("type")
    body = event.get("payload")
    if not isinstance(body, dict):
        continue
    subtype = body.get("type")
    if kind == "response_item" and subtype in {
        "function_call",
        "function_call_output",
        "custom_tool_call",
        "custom_tool_call_output",
    }:
        if subtype in {"function_call", "custom_tool_call"}:
            name = body.get("name", subtype)
            arguments = body.get("arguments", body.get("input", ""))
            print(f"\nTRACE LINE {line_number}: {subtype} {name}\n{bounded(arguments)}")
        else:
            output = body.get("output", body.get("content", ""))
            print(f"\nTRACE LINE {line_number}: {subtype}\n{bounded(output)}")
    elif kind == "event_msg" and subtype in {
        "agent_message",
        "task_complete",
        "user_message",
        "web_search_end",
    }:
        message = body.get(
            "message",
            body.get("last_agent_message", body),
        )
        print(f"\nTRACE LINE {line_number}: event {subtype}\n{bounded(message)}")
