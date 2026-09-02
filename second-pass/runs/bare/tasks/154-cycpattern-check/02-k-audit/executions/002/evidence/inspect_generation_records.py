#!/usr/bin/env python3
"""Parse the complete structured generation trace and summarize key claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T07-50-47-019f89e0-f031-7ce1-9a15-e5139d2b9cbd.jsonl"
)
records = []
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()

for number, line in enumerate(trace.read_text(encoding="utf-8").splitlines(), 1):
    record = json.loads(line)
    records.append((number, record))
    top_types[str(record.get("type"))] += 1
    payload = record.get("payload") or {}
    payload_types[str(payload.get("type"))] += 1

print(f"trace_records={len(records)}")
print(f"top_type_counts={dict(sorted(top_types.items()))}")
print(f"payload_type_counts={dict(sorted(payload_types.items()))}")

for number, record in records:
    payload = record.get("payload") or {}
    if payload.get("type") == "message" and payload.get("role") == "assistant":
        text = " ".join(
            item.get("text", "")
            for item in payload.get("content", [])
            if isinstance(item, dict)
        )
        if (
            "empty-second-word behavior" in text
            or "961 exhaustive small-string" in text
            or "Implemented all deliverables" in text
        ):
            print(f"assistant_message_line={number} text={text}")

for number, record in records:
    payload = record.get("payload") or {}
    if payload.get("type") == "custom_tool_call":
        tool_input = payload.get("input", "")
        if "Python examples and {len(words) ** 2} exhaustive pairs passed" in tool_input:
            print(f"generation_differential_call_line={number}")
            start = tool_input.index("from itertools import product")
            end = tool_input.index("python3 py2mpy.py", start)
            print(tool_input[start:end].replace("\\n", "\n"))
    if payload.get("type") == "custom_tool_call_output":
        text = str(payload.get("output", ""))
        if "Python examples and 961 exhaustive pairs passed" in text:
            print(f"generation_differential_output_line={number}")
            print("Python examples and 961 exhaustive pairs passed")

output_log = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8"
)
last = Path("/generation-evidence/codex-last.txt").read_text(encoding="utf-8")
prompt = Path("/generation-evidence/prompt.txt").read_text(encoding="utf-8")
print(f"codex_output_chars={len(output_log)} lines={len(output_log.splitlines())}")
print(f"codex_last_chars={len(last)} lines={len(last.splitlines())}")
print(f"generation_prompt_chars={len(prompt)} lines={len(prompt.splitlines())}")
print(
    "codex_output_has_kprove_passed="
    f"{'RESULT: KPROVE_PASSED' in output_log}"
)
print(
    "codex_last_has_kprove_passed="
    f"{'RESULT: KPROVE_PASSED' in last}"
)
