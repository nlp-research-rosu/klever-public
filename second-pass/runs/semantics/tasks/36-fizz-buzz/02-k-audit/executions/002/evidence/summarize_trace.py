#!/usr/bin/env python3
"""Parse every structured-trace record and summarize untrusted generation claims."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T23-05-54-019f8d26-be15-7193-af5e-cbed9f66562d.jsonl"
)

top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
roles: Counter[str] = Counter()
tool_calls: list[tuple[int, str, str]] = []
tool_outputs: list[tuple[int, str, str]] = []
agent_messages: list[tuple[int, str, str]] = []
parse_errors: list[tuple[int, str]] = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            event = json.loads(line)
        except Exception as err:  # pragma: no cover - evidence path
            parse_errors.append((line_number, repr(err)))
            continue
        top_type = str(event.get("type"))
        top_types[top_type] += 1
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        role = payload.get("role")
        if role is not None:
            roles[str(role)] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            name = str(payload.get("name", payload.get("call_id", "<unknown>")))
            arguments = str(payload.get("arguments", payload.get("input", "")))
            tool_calls.append((line_number, name, arguments))
        if payload_type in {"function_call_output", "custom_tool_call_output"}:
            call_id = str(payload.get("call_id", "<unknown>"))
            output = str(payload.get("output", ""))
            tool_outputs.append((line_number, call_id, output))
        if payload_type == "agent_message":
            agent_messages.append(
                (
                    line_number,
                    str(payload.get("phase", "")),
                    str(payload.get("message", "")),
                )
            )

print(f"trace_lines={sum(top_types.values()) + len(parse_errors)}")
print(f"parse_errors={parse_errors}")
print(f"top_level_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"message_roles={dict(sorted(roles.items()))}")
print(f"tool_call_count={len(tool_calls)}")
print(f"tool_output_count={len(tool_outputs)}")
print("TOOL_CALLS_BEGIN")
for line_number, name, arguments in tool_calls:
    one_line = arguments.replace("\n", "\\n")
    if len(one_line) > 1000:
        one_line = one_line[:1000] + "...<truncated>"
    print(f"line={line_number} name={name} args={one_line}")
print("TOOL_CALLS_END")
print("TOOL_OUTPUT_STATUS_SUMMARY_BEGIN")
for line_number, call_id, output in tool_outputs:
    first_lines = output.splitlines()[:5]
    short = "\\n".join(first_lines)
    if len(short) > 800:
        short = short[:800] + "...<truncated>"
    print(f"line={line_number} call_id={call_id} output_prefix={short}")
print("TOOL_OUTPUT_STATUS_SUMMARY_END")
print("AGENT_MESSAGES_BEGIN")
for line_number, phase, message in agent_messages:
    one_line = message.replace("\n", "\\n")
    if len(one_line) > 2000:
        one_line = one_line[:2000] + "...<truncated>"
    print(f"line={line_number} phase={phase} message={one_line}")
print("AGENT_MESSAGES_END")
