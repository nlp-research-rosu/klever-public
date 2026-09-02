#!/usr/bin/env python3
"""Summarize every JSONL record without trusting generation conclusions."""

import collections
import hashlib
import json
import sys


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def flatten_text(content) -> str:
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if isinstance(item, dict):
            value = item.get("text")
            if isinstance(value, str):
                parts.append(value)
    return "\n".join(parts)


path = sys.argv[1]
outer = collections.Counter()
inner = collections.Counter()
records = 0
parse_errors = 0
interesting = []

with open(path, encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        records += 1
        try:
            record = json.loads(line)
        except Exception as err:
            parse_errors += 1
            interesting.append((line_number, f"PARSE_ERROR {err}"))
            continue
        record_type = str(record.get("type"))
        outer[record_type] += 1
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type"))
        inner[(record_type, payload_type)] += 1
        if record_type == "response_item":
            if payload_type == "custom_tool_call":
                raw = payload.get("input", "")
                if not isinstance(raw, str):
                    raw = json.dumps(raw, sort_keys=True)
                preview = raw[:3000].replace("\x00", "\\0")
                interesting.append(
                    (
                        line_number,
                        "TOOL "
                        f"name={payload.get('name')} chars={len(raw)} "
                        f"sha256={digest(raw)}\n{preview}",
                    )
                )
            elif payload_type == "custom_tool_call_output":
                raw = json.dumps(payload.get("output"), sort_keys=True)
                interesting.append(
                    (
                        line_number,
                        "TOOL_OUTPUT "
                        f"chars={len(raw)} sha256={digest(raw)}\n{raw[:3000]}",
                    )
                )
            elif payload_type == "message":
                text = flatten_text(payload.get("content"))
                interesting.append(
                    (
                        line_number,
                        "MESSAGE "
                        f"role={payload.get('role')} chars={len(text)} "
                        f"sha256={digest(text)}\n{text[:1500]}",
                    )
                )
        elif record_type == "event_msg" and payload_type in {
            "agent_message",
            "task_started",
            "task_complete",
            "turn_aborted",
        }:
            raw = json.dumps(payload, sort_keys=True)
            interesting.append(
                (
                    line_number,
                    f"EVENT {payload_type} chars={len(raw)} sha256={digest(raw)}\n"
                    f"{raw[:2000]}",
                )
            )

print(f"PATH: {path}")
print(f"RECORDS: {records}")
print(f"PARSE_ERRORS: {parse_errors}")
print("OUTER_COUNTS:")
for key, value in sorted(outer.items()):
    print(f"  {key}: {value}")
print("OUTER_INNER_COUNTS:")
for key, value in sorted(inner.items()):
    print(f"  {key[0]}/{key[1]}: {value}")
print("INTERESTING_RECORDS:")
for line_number, body in interesting:
    print(f"--- LINE {line_number} ---")
    print(body)
