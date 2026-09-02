#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_paths = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"TRACE FILES: {len(trace_paths)}")
for trace_path in trace_paths:
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    final_texts: list[str] = []
    malformed = 0
    line_count = 0
    for line_count, line in enumerate(
        trace_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        outer_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if payload_type == "custom_tool_call":
            tool_names[str(payload.get("name"))] += 1
        if payload_type == "message" and payload.get("role") == "assistant":
            for content in payload.get("content", []):
                if isinstance(content, dict) and content.get("type") == "output_text":
                    final_texts.append(str(content.get("text", "")))
    print(f"PATH: {trace_path}")
    print(f"BYTES: {trace_path.stat().st_size}")
    print(f"LINES: {line_count}")
    print(f"MALFORMED JSON LINES: {malformed}")
    print(f"OUTER TYPES: {dict(sorted(outer_types.items()))}")
    print(f"PAYLOAD TYPES: {dict(sorted(payload_types.items()))}")
    print(f"TOOL NAMES: {dict(sorted(tool_names.items()))}")
    print(f"ASSISTANT OUTPUT TEXT RECORDS: {len(final_texts)}")
    for index, text in enumerate(final_texts[-3:], start=max(0, len(final_texts) - 3)):
        bounded_text = text if len(text) <= 2_000 else text[:2_000] + "…[truncated]"
        print(f"ASSISTANT OUTPUT {index}: {bounded_text!r}")
