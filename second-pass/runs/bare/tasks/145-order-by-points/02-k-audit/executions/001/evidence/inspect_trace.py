#!/usr/bin/env python3
"""Parse every record in the untrusted generation trace and summarize claims."""

from __future__ import annotations

import collections
import glob
import hashlib
import json


def excerpt(value, limit=600):
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    clean = text.replace("\x00", "\\0")
    if len(clean) <= limit:
        return clean
    return clean[: limit // 2] + "\n...[bounded]...\n" + clean[-limit // 2 :]


def normalized(value):
    return value if isinstance(value, str) else json.dumps(value, sort_keys=True)


paths = glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True)
print(f"trace_files={len(paths)}")
for path in sorted(paths):
    raw = open(path, "rb").read()
    print(f"path={path}")
    print(f"bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")
    top_types = collections.Counter()
    payload_types = collections.Counter()
    parsed = []
    parse_errors = []
    for number, line in enumerate(raw.splitlines(), 1):
        try:
            obj = json.loads(line)
        except Exception as error:
            parse_errors.append((number, repr(error)))
            continue
        parsed.append((number, obj))
        top_types[obj.get("type", "<missing>")] += 1
        payload = obj.get("payload", {})
        payload_types[payload.get("type", "<missing>")] += 1
    print(f"records={len(parsed)} parse_errors={parse_errors}")
    print(f"top_types={dict(top_types)}")
    print(f"payload_types={dict(payload_types)}")

    for number, obj in parsed:
        payload = obj.get("payload", {})
        subtype = payload.get("type")
        if obj.get("type") == "session_meta":
            fields = {
                key: payload.get(key)
                for key in ("session_id", "timestamp", "cwd", "cli_version", "model_provider")
            }
            print(f"RECORD {number} SESSION {json.dumps(fields, sort_keys=True)}")
        elif subtype in ("function_call", "custom_tool_call"):
            print(
                f"RECORD {number} TOOL_CALL name={payload.get('name')} "
                f"call_id={payload.get('call_id')} "
                f"input={excerpt(payload.get('input', payload.get('arguments')))}"
            )
        elif subtype in ("function_call_output", "custom_tool_call_output"):
            output = normalized(payload.get("output", ""))
            print(
                f"RECORD {number} TOOL_OUTPUT call_id={payload.get('call_id')} "
                f"chars={len(output)} sha256={hashlib.sha256(output.encode()).hexdigest()} "
                f"excerpt={excerpt(output)}"
            )
        elif subtype == "message" and payload.get("role") in ("user", "assistant"):
            print(
                f"RECORD {number} MESSAGE role={payload.get('role')} "
                f"phase={payload.get('phase')} content={excerpt(payload.get('content'), 1400)}"
            )
        elif obj.get("type") == "event_msg" and subtype in (
            "agent_message",
            "task_complete",
            "turn_aborted",
        ):
            print(
                f"RECORD {number} EVENT subtype={subtype} "
                f"message={excerpt(payload.get('message'), 1400)}"
            )
