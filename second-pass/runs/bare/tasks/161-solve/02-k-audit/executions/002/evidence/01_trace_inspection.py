#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T08-01-45-019f89ea-f6f2-71c1-85b5-d5ec0f90f188.jsonl"
)

outer = collections.Counter()
payloads = collections.Counter()
timestamps = []
calls = []
messages = []
parse_errors = []

for line_number, line in enumerate(TRACE.read_text().splitlines(), 1):
    try:
        record = json.loads(line)
    except Exception as err:
        parse_errors.append((line_number, repr(err)))
        continue
    outer[record.get("type")] += 1
    timestamps.append(record.get("timestamp"))
    payload = record.get("payload", {})
    payload_type = payload.get("type")
    payloads[(record.get("type"), payload_type)] += 1
    if payload_type in {"custom_tool_call", "function_call"}:
        name = (
            payload.get("name")
            or payload.get("tool_name")
            or payload.get("function", {}).get("name")
        )
        arguments = payload.get("arguments") or payload.get("input") or ""
        if not isinstance(arguments, str):
            arguments = json.dumps(arguments, sort_keys=True)
        calls.append((line_number, name, arguments))
    if payload_type in {"message", "agent_message", "user_message"}:
        content = payload.get("content") or payload.get("message") or ""
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False, sort_keys=True)
        messages.append((line_number, payload_type, content))

print("trace_path=", TRACE)
print("parsed_line_count=", sum(outer.values()))
print("parse_error_count=", len(parse_errors))
print("outer_type_counts=", dict(sorted(outer.items())))
print(
    "payload_type_counts=",
    {f"{a}/{b}": n for (a, b), n in sorted(payloads.items(), key=str)},
)
print("first_timestamp=", next((x for x in timestamps if x), None))
print("last_timestamp=", next((x for x in reversed(timestamps) if x), None))
print("tool_call_count=", len(calls))
for line_number, name, arguments in calls:
    one_line = " ".join(arguments.split())
    print(
        f"TOOL line={line_number} name={name!r} "
        f"arguments_prefix={one_line[:320]!r}"
    )
print("message_count=", len(messages))
for line_number, payload_type, content in messages:
    one_line = " ".join(content.split())
    print(
        f"MESSAGE line={line_number} type={payload_type} "
        f"content_prefix={one_line[:500]!r}"
    )
for error in parse_errors:
    print("PARSE_ERROR", error)

output = Path("/generation-evidence/codex-output.log").read_text(errors="replace")
last = Path("/generation-evidence/codex-last.txt").read_text(errors="replace")
print("codex_output_char_count=", len(output))
print("codex_output_line_count=", len(output.splitlines()))
print("codex_output_top_count=", output.count("#Top"))
print("codex_output_kprove_passed_count=", output.count("KPROVE_PASSED"))
print("codex_last=", " ".join(last.split()))

raise SystemExit(1 if parse_errors else 0)
