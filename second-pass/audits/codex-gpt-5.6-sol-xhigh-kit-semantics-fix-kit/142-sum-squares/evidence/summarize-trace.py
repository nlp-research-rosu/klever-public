#!/usr/bin/env python3
"""Read an untrusted Codex JSONL trace and print a bounded structural summary."""

import collections
import json
import sys


path = sys.argv[1]
event_types = collections.Counter()
payload_types = collections.Counter()
roles = collections.Counter()
tool_names = collections.Counter()
assistant_messages = []
lines = 0

with open(path, encoding="utf-8") as trace:
    for raw in trace:
        lines += 1
        event = json.loads(raw)
        event_types[event.get("type", "<none>")] += 1
        payload = event.get("payload") or {}
        payload_types[payload.get("type", "<none>")] += 1
        roles[payload.get("role", "<none>")] += 1
        if payload.get("type") in {"function_call", "custom_tool_call"}:
            tool_names[payload.get("name", "<none>")] += 1
        if payload.get("type") == "message" and payload.get("role") == "assistant":
            text_parts = []
            for item in payload.get("content") or []:
                if item.get("type") in {"output_text", "input_text"}:
                    text_parts.append(item.get("text", ""))
            if text_parts:
                assistant_messages.append("\n".join(text_parts))

print(f"FILE: {path}")
print(f"LINES_READ: {lines}")
print(f"EVENT_TYPES: {dict(event_types)}")
print(f"PAYLOAD_TYPES: {dict(payload_types)}")
print(f"ROLES: {dict(roles)}")
print(f"TOOL_NAMES: {dict(tool_names)}")
print(f"ASSISTANT_MESSAGES: {len(assistant_messages)}")
if assistant_messages:
    final = assistant_messages[-1]
    print("FINAL_ASSISTANT_MESSAGE_BEGIN")
    print(final[:12000])
    if len(final) > 12000:
        print(f"[TRUNCATED {len(final) - 12000} CHARACTERS]")
    print("FINAL_ASSISTANT_MESSAGE_END")
