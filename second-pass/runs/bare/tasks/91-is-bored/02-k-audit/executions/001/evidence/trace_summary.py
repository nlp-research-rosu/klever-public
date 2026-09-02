#!/usr/bin/env python3
"""Bounded extraction of claims from the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-04-20-019f897f-78ae-75b2-b2be-2505838c95bf.jsonl"
)
counts: collections.Counter[str] = collections.Counter()
selected: list[str] = []

with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        record_type = str(record.get("type"))
        counts[record_type] += 1
        payload = record.get("payload", {})
        payload_type = str(payload.get("type"))
        counts[f"{record_type}/{payload_type}"] += 1

        if payload_type == "agent_message":
            message = str(payload.get("message", ""))
            if any(
                needle in message
                for needle in ("#Top", "kprove", "10,000", "RESULT:")
            ):
                selected.append(
                    f"line={line_number} agent_message={message[:1200]!r}"
                )
        elif payload_type == "message" and payload.get("role") == "assistant":
            text = " ".join(
                str(part.get("text", ""))
                for part in payload.get("content", [])
                if isinstance(part, dict)
            )
            if any(needle in text for needle in ("#Top", "kprove", "RESULT:")):
                selected.append(f"line={line_number} assistant={text[:1200]!r}")
        elif payload_type == "custom_tool_call":
            tool_input = str(payload.get("input", ""))
            if any(
                needle in tool_input
                for needle in ("kprove", "kompile", "krun", "range(10000)")
            ):
                selected.append(
                    f"line={line_number} tool_call={tool_input[:1800]!r}"
                )
        elif payload_type == "custom_tool_call_output":
            output_text = repr(payload.get("output", ""))
            if any(
                needle in output_text
                for needle in ("#Top", "passed", "backend terminated")
            ):
                selected.append(
                    f"line={line_number} tool_output={output_text[:1800]}"
                )

print(f"trace={trace}")
print(f"record_count={sum(value for key, value in counts.items() if '/' not in key)}")
for key in sorted(counts):
    print(f"count[{key}]={counts[key]}")
print(f"selected_count={len(selected)}")
for item in selected:
    print(item)
