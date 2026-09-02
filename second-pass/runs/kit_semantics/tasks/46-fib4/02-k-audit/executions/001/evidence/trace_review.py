#!/usr/bin/env python3
"""Read the full structured trace and summarize all observable event payloads."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-13-42-019f97b1-8ab1-7550-a558-f16a2783a5af.jsonl"
)


def compact(value: object, limit: int = 2000) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(text) > limit:
        return text[:limit] + f"... [truncated; {len(text)} chars total]"
    return text


def main() -> None:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_calls: list[tuple[int, str, object]] = []
    agent_messages: list[tuple[int, object]] = []
    user_messages: list[tuple[int, object]] = []
    outputs: list[tuple[int, str, int]] = []
    parse_errors: list[str] = []

    with TRACE.open() as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                parse_errors.append(f"line {line_number}: {error}")
                continue
            top_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                subtype = str(payload.get("type"))
                payload_types[subtype] += 1
                if subtype in ("custom_tool_call", "function_call"):
                    name = str(payload.get("name"))
                    args = payload.get("input", payload.get("arguments"))
                    tool_calls.append((line_number, name, args))
                elif subtype == "agent_message":
                    agent_messages.append((line_number, payload.get("message")))
                elif subtype == "user_message":
                    user_messages.append((line_number, payload.get("message")))
                elif subtype in ("custom_tool_call_output", "function_call_output"):
                    rendered = compact(payload.get("output"), 1000000)
                    outputs.append((line_number, str(payload.get("call_id")), len(rendered)))

    print(f"TRACE={TRACE}")
    print(f"lines={sum(top_types.values())} parse_errors={len(parse_errors)}")
    print(f"top_types={dict(top_types)}")
    print(f"payload_types={dict(payload_types)}")
    print(f"user_messages={len(user_messages)} agent_messages={len(agent_messages)}")
    print(f"tool_calls={len(tool_calls)} tool_outputs={len(outputs)}")
    for error in parse_errors:
        print(f"PARSE_ERROR {error}")

    print("\nAGENT MESSAGES")
    for line_number, message in agent_messages:
        print(f"LINE {line_number}: {compact(message, 8000)}")

    print("\nTOOL CALLS")
    for line_number, name, args in tool_calls:
        print(f"LINE {line_number} {name}: {compact(args, 12000)}")

    print("\nTOOL OUTPUT SIZE INVENTORY")
    for line_number, call_id, size in outputs:
        print(f"LINE {line_number} call_id={call_id} rendered_chars={size}")


if __name__ == "__main__":
    main()
