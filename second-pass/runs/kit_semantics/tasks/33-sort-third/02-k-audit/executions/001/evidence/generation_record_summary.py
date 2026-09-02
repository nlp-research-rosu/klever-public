#!/usr/bin/env python3
"""Read all pipeline-v3 generation records and summarize untrusted trace claims."""

from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter


root = pathlib.Path("/generation-evidence")
json_records = [
    pathlib.Path("/run.json"),
    pathlib.Path("/task.json"),
    pathlib.Path("/generation-result.json"),
    root / "invocation.json",
    root / "metrics.json",
    root / "runtime-metrics.json",
    root / "usage.json",
]
print("JSON_RECORDS")
for path in json_records:
    document = json.loads(path.read_text(encoding="utf-8"))
    print(
        f"{path}: type={type(document).__name__} "
        f"keys={','.join(sorted(document))}"
    )

for path in [root / "codex-last.txt", root / "codex-output.log", root / "prompt.txt"]:
    content = path.read_bytes()
    print(
        f"TEXT_RECORD {path}: bytes={len(content)} "
        f"lines={content.count(bytes([10]))} sha256={hashlib.sha256(content).hexdigest()}"
    )

outer_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
message_roles: Counter[str] = Counter()
function_names: Counter[str] = Counter()
assistant_messages: list[str] = []
trace_files = sorted((root / "codex-trace").rglob("*.jsonl"))
for path in trace_files:
    for line in path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        outer_types[str(event.get("type"))] += 1
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        role = payload.get("role")
        if isinstance(role, str):
            message_roles[role] += 1
        name = payload.get("name")
        if isinstance(name, str):
            function_names[name] += 1
        if payload_type == "message" and role == "assistant":
            text_parts = [
                part.get("text", "")
                for part in payload.get("content", [])
                if isinstance(part, dict) and isinstance(part.get("text"), str)
            ]
            if text_parts:
                assistant_messages.append("\n".join(text_parts))
print(f"TRACE_FILES={len(trace_files)}")
print(f"OUTER_TYPES={dict(sorted(outer_types.items()))}")
print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
print(f"MESSAGE_ROLES={dict(sorted(message_roles.items()))}")
print(f"FUNCTION_NAMES={dict(sorted(function_names.items()))}")
print(f"ASSISTANT_MESSAGE_COUNT={len(assistant_messages)}")
if assistant_messages:
    final = assistant_messages[-1]
    print(f"FINAL_ASSISTANT_MESSAGE_SHA256={hashlib.sha256(final.encode()).hexdigest()}")
    print("FINAL_ASSISTANT_MESSAGE_BEGIN")
    print(final)
    print("FINAL_ASSISTANT_MESSAGE_END")
