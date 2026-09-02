#!/usr/bin/env python3
"""Parse every generation trace event and emit a bounded semantic summary."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T03-10-29-019facec-d1db-7801-97a0-88b8a1f5ac4a.jsonl"
)


def bounded(value: object, limit: int = 1800) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:900] + f"\n... [{len(text) - 1800} chars omitted] ...\n" + text[-900:]


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/generation_trace_summary.py")
    events = []
    with TRACE.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            events.append((line_number, json.loads(line)))
    print(f"parsed_json_lines={len(events)}")
    for line_number, event in events:
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type")
        if payload_type in {
            "function_call",
            "custom_tool_call",
            "agent_message",
            "user_message",
            "task_complete",
        }:
            print(
                f"\nTRACE_LINE={line_number} TIMESTAMP={event.get('timestamp')} "
                f"PAYLOAD_TYPE={payload_type}"
            )
            if payload_type == "function_call":
                print(f"name={payload.get('name')} call_id={payload.get('call_id')}")
                print(f"arguments={bounded(payload.get('arguments'))}")
            elif payload_type == "custom_tool_call":
                print(f"name={payload.get('name')} call_id={payload.get('call_id')}")
                print(f"input={bounded(payload.get('input'))}")
            else:
                material = {
                    key: payload.get(key)
                    for key in ("message", "last_agent_message", "phase")
                    if key in payload
                }
                print(bounded(material))
    print("\nSTATUS: FULL TRACE PARSED; SELECTED EVENTS SUMMARIZED")


if __name__ == "__main__":
    main()
