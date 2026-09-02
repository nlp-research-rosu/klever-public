#!/usr/bin/env python3
"""Parse every event in the untrusted generation trace into a bounded audit summary."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def bounded(value: object, limit: int = 1200) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x1b", "<ESC>")
    if len(text) <= limit:
        return text
    half = limit // 2
    return f"{text[:half]}\n... <{len(text) - limit} chars omitted> ...\n{text[-half:]}"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 2

    trace = pathlib.Path(sys.argv[1])
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    parsed = 0

    for line_number, line in enumerate(trace.open(encoding="utf-8"), 1):
        event = json.loads(line)
        parsed += 1
        top_type = str(event.get("type"))
        top_types[top_type] += 1
        payload = event.get("payload", {})
        payload_type = str(payload.get("type")) if isinstance(payload, dict) else "-"
        payload_types[payload_type] += 1

        if top_type == "response_item" and isinstance(payload, dict):
            if payload_type == "function_call":
                print(
                    f"EVENT {line_number} function_call "
                    f"name={payload.get('name')} id={payload.get('call_id')}"
                )
                print(bounded(payload.get("arguments", ""), 2400))
            elif payload_type == "function_call_output":
                print(
                    f"EVENT {line_number} function_output "
                    f"id={payload.get('call_id')}"
                )
                print(bounded(payload.get("output", ""), 1600))
            elif payload_type == "message" and payload.get("role") == "assistant":
                texts = [
                    item.get("text", "")
                    for item in payload.get("content", [])
                    if isinstance(item, dict) and item.get("type") in {"output_text", "input_text"}
                ]
                if texts:
                    print(f"EVENT {line_number} assistant_message")
                    print(bounded("\n".join(texts), 1600))
        elif top_type == "event_msg" and isinstance(payload, dict):
            if payload_type in {"task_complete", "agent_message", "turn_aborted"}:
                print(f"EVENT {line_number} event_msg type={payload_type}")
                print(bounded(payload, 1600))

    print(f"PARSED_JSON_LINES={parsed}")
    print("TOP_LEVEL_TYPES=" + json.dumps(dict(sorted(top_types.items())), sort_keys=True))
    print("PAYLOAD_TYPES=" + json.dumps(dict(sorted(payload_types.items())), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
