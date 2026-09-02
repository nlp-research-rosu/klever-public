#!/usr/bin/env python3
"""Bounded human-readable extraction of the untrusted generation trace."""

import collections
import json
import pathlib

TRACE = pathlib.Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T03-47-50-019f8902-81a0-7132-bf36-6f07efd73d96.jsonl"
)

counts = collections.Counter()
records = []
with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        obj = json.loads(line)
        outer_type = obj.get("type", "")
        payload = obj.get("payload", {})
        inner_type = payload.get("type", "") if isinstance(payload, dict) else ""
        counts[(outer_type, inner_type)] += 1
        if outer_type != "response_item" or not isinstance(payload, dict):
            continue
        if inner_type == "message":
            role = payload.get("role", "")
            text = "\n".join(
                part.get("text", "")
                for part in payload.get("content", [])
                if isinstance(part, dict)
            )
            # Preserve the candidate's own conversational work; omit bulky
            # repeated system/developer scaffolding from this bounded extract.
            if role in {"assistant", "user"}:
                records.append((line_number, f"MESSAGE {role}", text))
        elif inner_type == "function_call":
            records.append(
                (
                    line_number,
                    f"CALL {payload.get('name', '')}",
                    str(payload.get("arguments", "")),
                )
            )
        elif inner_type == "function_call_output":
            output = str(payload.get("output", ""))
            if len(output) > 4000:
                output = output[:2000] + "\n...[bounded extract]...\n" + output[-2000:]
            records.append(
                (
                    line_number,
                    f"OUTPUT {payload.get('call_id', '')}",
                    output,
                )
            )
        elif inner_type == "custom_tool_call":
            records.append(
                (
                    line_number,
                    f"CUSTOM CALL {payload.get('name', '')}",
                    str(payload.get("input", "")),
                )
            )
        elif inner_type == "custom_tool_call_output":
            chunks = payload.get("output", [])
            output = "\n".join(
                part.get("text", "")
                for part in chunks
                if isinstance(part, dict)
            )
            if len(output) > 4000:
                output = output[:2000] + "\n...[bounded extract]...\n" + output[-2000:]
            records.append(
                (
                    line_number,
                    f"CUSTOM OUTPUT {payload.get('call_id', '')}",
                    output,
                )
            )

print("TRACE:", TRACE)
print("COUNTS:")
for key, value in sorted(counts.items()):
    print(f"  {key[0]}/{key[1]}: {value}")
print("CANDIDATE WORK RECORDS:")
for line_number, label, text in records:
    print(f"\n[{line_number}] {label}")
    print(text)
