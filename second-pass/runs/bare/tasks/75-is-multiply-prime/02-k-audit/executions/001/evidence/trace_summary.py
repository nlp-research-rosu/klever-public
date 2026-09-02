#!/usr/bin/env python3
"""Read the complete untrusted JSONL trace and print a bounded audit summary."""

from __future__ import annotations

import collections
import glob
import hashlib
import json


def text_content(content: object) -> str:
    if not isinstance(content, list):
        return repr(content)
    parts: list[str] = []
    for item in content:
        if isinstance(item, dict):
            value = item.get("text")
            if isinstance(value, str):
                parts.append(value)
    return "\n".join(parts)


for path in sorted(glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True)):
    digest = hashlib.sha256()
    type_counts: collections.Counter[str] = collections.Counter()
    response_counts: collections.Counter[str] = collections.Counter()
    records: list[dict[str, object]] = []
    with open(path, "rb") as raw:
        for line_number, raw_line in enumerate(raw, 1):
            digest.update(raw_line)
            item = json.loads(raw_line)
            records.append(item)
            top_type = str(item.get("type", "<missing>"))
            type_counts[top_type] += 1
            if top_type == "response_item":
                payload = item.get("payload", {})
                if isinstance(payload, dict):
                    response_counts[str(payload.get("type", "<missing>"))] += 1

    print(f"TRACE {path}")
    print(f"lines={len(records)} sha256={digest.hexdigest()}")
    print(f"top_types={dict(sorted(type_counts.items()))}")
    print(f"response_types={dict(sorted(response_counts.items()))}")

    print("ASSISTANT_MESSAGES_AND_GENERATION_ACTIONS")
    for line_number, item in enumerate(records, 1):
        if item.get("type") != "response_item":
            continue
        payload = item.get("payload", {})
        if not isinstance(payload, dict):
            continue
        item_type = payload.get("type")
        role = payload.get("role")
        if item_type == "message" and role == "assistant":
            message = text_content(payload.get("content"))
            print(f"line={line_number} assistant_message={message!r}")
        elif item_type in {"custom_tool_call", "function_call"}:
            name = payload.get("name")
            arguments = payload.get("input", payload.get("arguments"))
            print(f"line={line_number} call={name!r} args={arguments!r}")
        elif item_type in {"custom_tool_call_output", "function_call_output"}:
            output = str(payload.get("output", ""))
            if len(output) > 4000:
                output = output[:2000] + "\n...[bounded]...\n" + output[-2000:]
            print(f"line={line_number} call_output={output!r}")
