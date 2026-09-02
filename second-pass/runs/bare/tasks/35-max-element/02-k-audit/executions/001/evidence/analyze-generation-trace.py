#!/usr/bin/env python3
"""Read every untrusted generation-log record and emit an audit-oriented digest."""

from __future__ import annotations

import collections
import json
from pathlib import Path

TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-42-06-019f8934-2f87-76d2-9959-2daa15c3fc06.jsonl"
)
PLAIN = Path("/candidate/codex-output.log")


def main() -> None:
    event_types: collections.Counter[str] = collections.Counter()
    response_types: collections.Counter[str] = collections.Counter()
    tools: collections.Counter[str] = collections.Counter()
    commands: list[str] = []
    assistant_messages: list[str] = []

    trace_lines = 0
    with TRACE.open(encoding="utf-8") as stream:
        for trace_lines, line in enumerate(stream, 1):
            record = json.loads(line)
            event_type = str(record.get("type"))
            event_types[event_type] += 1
            payload = record.get("payload", {})
            if event_type == "response_item":
                response_type = str(payload.get("type"))
                response_types[response_type] += 1
                if response_type == "custom_tool_call":
                    tools[str(payload.get("name"))] += 1
                    raw_input = payload.get("input")
                    if isinstance(raw_input, str):
                        commands.append(raw_input.replace("\n", "\\n"))
                if response_type == "message" and payload.get("role") == "assistant":
                    content = payload.get("content", [])
                    assistant_messages.extend(
                        item.get("text", "")
                        for item in content
                        if isinstance(item, dict) and isinstance(item.get("text"), str)
                    )

    plain_lines = 0
    markers: collections.Counter[str] = collections.Counter()
    with PLAIN.open(encoding="utf-8", errors="replace") as stream:
        for plain_lines, line in enumerate(stream, 1):
            for marker in (
                "kompile",
                "kprove",
                "krun",
                "#Top",
                "WarnStuckClaimState",
                "RESULT:",
                "apply_patch",
            ):
                if marker in line:
                    markers[marker] += 1

    print(f"trace_path={TRACE}")
    print(f"trace_lines_read={trace_lines}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_response_types={dict(sorted(response_types.items()))}")
    print(f"trace_tools={dict(sorted(tools.items()))}")
    print(f"plain_path={PLAIN}")
    print(f"plain_lines_read={plain_lines}")
    print(f"plain_marker_counts={dict(sorted(markers.items()))}")
    print("tool_call_inputs_begin")
    for index, command in enumerate(commands, 1):
        print(f"{index}: {command}")
    print("tool_call_inputs_end")
    print("assistant_messages_begin")
    for message in assistant_messages:
        print(message)
    print("assistant_messages_end")


if __name__ == "__main__":
    main()
