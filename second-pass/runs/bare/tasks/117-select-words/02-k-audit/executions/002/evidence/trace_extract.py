#!/usr/bin/env python3
"""Render every structured generation-trace tool call and result for review."""

from __future__ import annotations

import json
from pathlib import Path


def compact(value: object, limit: int = 8000) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated by reviewer at {limit}/{len(text)} chars]"


def main() -> None:
    trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    for line_no, line in enumerate(trace.read_text().splitlines(), 1):
        event = json.loads(line)
        payload = event.get("payload", {})
        ptype = payload.get("type") if isinstance(payload, dict) else None
        if event.get("type") == "response_item" and ptype in {
            "function_call",
            "function_call_output",
            "custom_tool_call",
            "custom_tool_call_output",
            "message",
        }:
            print(f"LINE {line_no} TYPE {ptype}")
            if ptype == "function_call":
                print("NAME", payload.get("name"))
                print("ARGS", compact(payload.get("arguments")))
            elif ptype == "function_call_output":
                print("CALL_ID", payload.get("call_id"))
                print("OUTPUT", compact(payload.get("output")))
            elif ptype == "custom_tool_call":
                print("NAME", payload.get("name"))
                print("INPUT", compact(payload.get("input")))
            elif ptype == "custom_tool_call_output":
                print("CALL_ID", payload.get("call_id"))
                print("OUTPUT", compact(payload.get("output")))
            else:
                print("ROLE", payload.get("role"))
                print("CONTENT", compact(payload.get("content")))
            print()


if __name__ == "__main__":
    main()
