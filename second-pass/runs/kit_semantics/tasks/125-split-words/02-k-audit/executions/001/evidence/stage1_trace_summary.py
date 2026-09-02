#!/usr/bin/env python3
"""Read and summarize the complete structured generation trace and text log."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT = Path("/generation-evidence/codex-output.log")

top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_names: Counter[str] = Counter()
session_ids: set[str] = set()
first_timestamp = None
last_timestamp = None
line_count = 0
final_messages: list[str] = []

for path in sorted(TRACE_ROOT.rglob("*.jsonl")):
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            line_count += 1
            timestamp = record.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            top_type = str(record.get("type"))
            top_types[top_type] += 1
            payload = record.get("payload") or {}
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if record.get("type") == "session_meta":
                session_ids.add(str(payload.get("session_id")))
            if payload_type in {"function_call", "custom_tool_call"}:
                tool_names[str(payload.get("name"))] += 1
            if payload_type == "message" and payload.get("role") == "assistant":
                content = payload.get("content") or []
                text = "\n".join(
                    str(item.get("text", ""))
                    for item in content
                    if isinstance(item, dict) and item.get("type") in {"output_text", "text"}
                )
                if text:
                    final_messages.append(text)

output_text = OUTPUT.read_text(errors="replace")
print("trace_jsonl_files=", len(list(TRACE_ROOT.rglob("*.jsonl"))))
print("trace_records=", line_count)
print("trace_first_timestamp=", first_timestamp)
print("trace_last_timestamp=", last_timestamp)
print("trace_session_ids=", sorted(session_ids))
print("trace_top_types=", dict(sorted(top_types.items())))
print("trace_payload_types=", dict(sorted(payload_types.items())))
print("trace_tool_names=", dict(sorted(tool_names.items())))
print("assistant_message_count=", len(final_messages))
if final_messages:
    print("last_assistant_message=", repr(final_messages[-1][:1000]))
print("codex_output_bytes=", OUTPUT.stat().st_size)
print("codex_output_lines=", output_text.count("\n") + (not output_text.endswith("\n")))
for needle in [
    "kompile",
    "kprove",
    "#Top",
    "WarnStuckClaimState",
    "RESULT: KPROVE_PASSED",
    "VALIDATED",
]:
    print(f"codex_output_occurrences[{needle!r}]=", output_text.count(needle))
