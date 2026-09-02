#!/usr/bin/env python3
"""Produce a bounded structural summary of the untrusted Codex JSONL trace."""

from __future__ import annotations

import json
from pathlib import Path


def clipped(value: object, limit: int = 1200) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = text.replace("\n", "\\n")
    if len(text) > limit:
        return text[:limit] + f"...<clipped {len(text) - limit} chars>"
    return text


for trace in sorted(Path("/generation-evidence/codex-trace").rglob("*")):
    if not trace.is_file():
        continue
    print(f"TRACE {trace}")
    with trace.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            record = json.loads(line)
            record_type = record.get("type")
            payload = record.get("payload", {})
            payload_type = payload.get("type") if isinstance(payload, dict) else None
            summary: object
            if isinstance(payload, dict) and payload_type in {
                "function_call",
                "function_call_output",
                "custom_tool_call",
                "custom_tool_call_output",
            }:
                summary = payload
            elif isinstance(payload, dict) and payload_type == "message":
                summary = {
                    "role": payload.get("role"),
                    "phase": payload.get("phase"),
                    "content": payload.get("content"),
                }
            elif isinstance(payload, dict) and payload_type in {
                "agent_message",
                "agent_reasoning",
            }:
                summary = payload
            elif isinstance(payload, dict) and payload_type == "token_count":
                summary = payload
            else:
                summary = payload
            print(
                f"{number:04d} ts={record.get('timestamp')} "
                f"type={record_type} payload_type={payload_type} {clipped(summary)}"
            )
