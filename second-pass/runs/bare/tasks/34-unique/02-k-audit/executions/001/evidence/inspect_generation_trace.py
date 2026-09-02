#!/usr/bin/env python3
"""Summarize the complete untrusted JSONL generation trace without trusting it."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-41-12-019f8933-5cbd-7782-87fb-8b7be75e80e2.jsonl"
)


def main() -> int:
    record_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    malformed = []
    commands = []
    final_messages = []

    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                malformed.append((line_number, str(exc)))
                continue
            record_types[str(record.get("type", "<missing>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_types[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    commands.append(
                        (
                            line_number,
                            payload.get("name"),
                            payload.get("arguments") or payload.get("input"),
                        )
                    )
                if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                    final_messages.append((line_number, payload.get("message")))
                if payload_type == "message" and payload.get("phase") == "final_answer":
                    content = payload.get("content")
                    final_messages.append((line_number, content))

    print(f"trace={TRACE}")
    print(f"records={sum(record_types.values())}")
    print(f"malformed_json_records={len(malformed)}")
    print("record_types=" + json.dumps(dict(sorted(record_types.items())), sort_keys=True))
    print("payload_types=" + json.dumps(dict(sorted(payload_types.items())), sort_keys=True))
    print(f"tool_call_records={len(commands)}")
    for line_number, name, arguments in commands:
        print(f"tool_call_line={line_number} name={name} arguments={arguments}")
    print(f"final_message_records={len(final_messages)}")
    for line_number, message in final_messages:
        print(f"final_message_line={line_number} value={message}")
    if malformed:
        print(f"first_malformed={malformed[0]}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
