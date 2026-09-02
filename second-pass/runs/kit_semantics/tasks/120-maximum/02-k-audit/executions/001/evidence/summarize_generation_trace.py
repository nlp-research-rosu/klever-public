#!/usr/bin/env python3
"""Render the untrusted JSONL generation trace into a bounded audit summary."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T02-17-26-019f9822-d295-7933-8eb0-55ade593843c.jsonl"
)
LIMIT = 1600


def shorten(value: object) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\r", "")
    if len(text) > LIMIT:
        return text[:LIMIT] + f"\n...[truncated {len(text) - LIMIT} characters]"
    return text


def main() -> None:
    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            event = json.loads(line)
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            kind = payload.get("type")
            if kind in {"agent_message", "user_message"}:
                print(f"\nLINE {line_number} {event['type']} {kind}")
                print(shorten(payload.get("message", "")))
            elif kind == "message":
                role = payload.get("role")
                if role not in {"assistant", "user"}:
                    continue
                content = payload.get("content", [])
                texts = [
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict)
                    and item.get("type") in {"input_text", "output_text"}
                ]
                print(f"\nLINE {line_number} response_item message role={role}")
                print(shorten("\n".join(texts)))
            elif kind == "function_call":
                print(
                    f"\nLINE {line_number} response_item function_call "
                    f"name={payload.get('name')}"
                )
                print(shorten(payload.get("arguments", "")))
            elif kind == "custom_tool_call":
                print(
                    f"\nLINE {line_number} response_item custom_tool_call "
                    f"name={payload.get('name')}"
                )
                print(shorten(payload.get("input", "")))
            elif kind in {"function_call_output", "custom_tool_call_output"}:
                print(f"\nLINE {line_number} response_item {kind}")
                print(shorten(payload.get("output", "")))
            elif kind in {"task_started", "task_complete"}:
                print(f"\nLINE {line_number} {event['type']} {kind}")
                print(shorten(payload))


if __name__ == "__main__":
    main()
