#!/usr/bin/env python3
"""Validate and summarize every JSONL event in the untrusted generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T07-18-13-019f8ee9-77c1-73c2-84ab-883b53530ad9.jsonl"
)


def one_line(value: object, limit: int = 1200) -> str:
    text = str(value).replace("\r", "\\r").replace("\n", "\\n")
    if len(text) > limit:
        return text[:limit] + f"...[truncated {len(text) - limit} chars]"
    return text


top_counts: collections.Counter[str] = collections.Counter()
sub_counts: collections.Counter[str] = collections.Counter()
calls: dict[str, str] = {}
outputs: set[str] = set()

with TRACE.open(encoding="utf-8") as stream:
    for line_number, raw in enumerate(stream, 1):
        event = json.loads(raw)
        top_type = event.get("type", "<missing>")
        payload = event.get("payload", {})
        subtype = payload.get("type", "") if isinstance(payload, dict) else ""
        top_counts[top_type] += 1
        if subtype:
            sub_counts[f"{top_type}/{subtype}"] += 1

        stamp = event.get("timestamp", "")
        label = f"{line_number:03d} {stamp} {top_type}"
        if subtype:
            label += f"/{subtype}"

        detail = ""
        if top_type == "response_item" and isinstance(payload, dict):
            if payload.get("type") in ("function_call", "custom_tool_call"):
                call_id = str(payload.get("call_id", payload.get("id", "")))
                name = str(payload.get("name", ""))
                calls[call_id] = name
                detail = f" name={name} args={one_line(payload.get('arguments', payload.get('input', '')))}"
            elif payload.get("type") in ("function_call_output", "custom_tool_call_output"):
                call_id = str(payload.get("call_id", ""))
                outputs.add(call_id)
                detail = f" call_id={call_id} output={one_line(payload.get('output', ''))}"
            elif payload.get("type") == "message":
                detail = (
                    f" role={payload.get('role', '')} phase={payload.get('phase', '')}"
                    f" content={one_line(payload.get('content', ''))}"
                )
        elif top_type == "event_msg" and isinstance(payload, dict):
            for key in ("message", "last_agent_message"):
                if key in payload:
                    detail = f" {key}={one_line(payload[key])}"
                    break
        elif top_type == "session_meta" and isinstance(payload, dict):
            detail = (
                f" session_id={payload.get('session_id', '')}"
                f" cwd={payload.get('cwd', '')} cli={payload.get('cli_version', '')}"
            )
        print(label + detail)

print("TOP_COUNTS", dict(sorted(top_counts.items())))
print("SUBTYPE_COUNTS", dict(sorted(sub_counts.items())))
print("FUNCTION_CALLS", len(calls))
print("FUNCTION_OUTPUTS", len(outputs))
print("UNPAIRED_CALLS", sorted((call_id, calls[call_id]) for call_id in calls if call_id not in outputs))
