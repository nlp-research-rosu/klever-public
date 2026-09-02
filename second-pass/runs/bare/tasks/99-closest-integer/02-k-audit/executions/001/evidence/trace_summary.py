#!/usr/bin/env python3
"""Bounded structural summary of the untrusted candidate generation trace."""

from collections import Counter
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-18-41-019f898c-9b29-77b2-9431-b031fa9ae74a.jsonl"
)


def main() -> None:
    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    command_count = 0
    command_results = 0
    parse_failures = 0
    first_timestamp = None
    last_timestamp = None
    final_messages: list[str] = []

    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                parse_failures += 1
                print(f"PARSE_FAILURE line={line_number}: {error}")
                continue
            timestamp = record.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            outer_types[str(record.get("type", "<missing>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_types[payload_type] += 1
                if "role" in payload:
                    roles[str(payload["role"])] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    command_count += 1
                if payload_type in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    command_results += 1
                if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                    final_messages.append(str(payload.get("message", "")))

    print(f"TRACE={TRACE}")
    print(f"RECORDS={sum(outer_types.values())}")
    print(f"PARSE_FAILURES={parse_failures}")
    print(f"FIRST_TIMESTAMP={first_timestamp}")
    print(f"LAST_TIMESTAMP={last_timestamp}")
    print(f"OUTER_TYPES={dict(sorted(outer_types.items()))}")
    print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
    print(f"ROLES={dict(sorted(roles.items()))}")
    print(f"TOOL_CALL_RECORDS={command_count}")
    print(f"TOOL_RESULT_RECORDS={command_results}")
    print(f"FINAL_MESSAGE_COUNT={len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        print(f"FINAL_MESSAGE_{index}={message!r}")


if __name__ == "__main__":
    main()
