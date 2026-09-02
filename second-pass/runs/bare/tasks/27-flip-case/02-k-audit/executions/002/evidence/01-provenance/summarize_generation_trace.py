#!/usr/bin/env python3
"""Parse every structured trace record and summarize untrusted generation actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-26-46-019f8926-2706-76c1-9838-b7b318fd85d9.jsonl"
)


def compact(value: object, limit: int = 800) -> str:
    text = json.dumps(value, ensure_ascii=True, sort_keys=True)
    if len(text) > limit:
        return text[:limit] + f"...[truncated {len(text) - limit} chars]"
    return text


def main() -> None:
    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    tool_calls: list[tuple[int, str, str]] = []
    agent_messages: list[tuple[int, str]] = []
    parse_errors: list[tuple[int, str]] = []
    total = 0
    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            total += 1
            try:
                record = json.loads(line)
            except Exception as error:
                parse_errors.append((line_number, repr(error)))
                continue
            record_type = str(record.get("type"))
            type_counts[record_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_counts[payload_type] += 1
                if payload_type in {"custom_tool_call", "function_call"}:
                    tool_calls.append(
                        (
                            line_number,
                            str(payload.get("name")),
                            compact(payload.get("input", payload.get("arguments"))),
                        )
                    )
                if payload_type == "agent_message":
                    agent_messages.append(
                        (line_number, compact(payload.get("message"), 1200))
                    )
    print("trace", TRACE)
    print("line_count", total)
    print("parse_errors", parse_errors)
    print("record_type_counts", dict(sorted(type_counts.items())))
    print("payload_type_counts", dict(sorted(payload_counts.items())))
    print("tool_call_count", len(tool_calls))
    for line_number, name, tool_input in tool_calls:
        print(f"tool_call line={line_number} name={name} input={tool_input}")
    print("agent_message_count", len(agent_messages))
    for line_number, message in agent_messages:
        print(f"agent_message line={line_number} message={message}")


if __name__ == "__main__":
    main()
