#!/usr/bin/env python3
"""Read and summarize every structured generation-trace record."""

import json
from collections import Counter
from hashlib import sha256
from pathlib import Path


trace_paths = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
response_types = Counter()
event_types = Counter()
function_names = Counter()
roles = Counter()
assistant_messages = []
function_calls = 0
function_outputs = 0

for path in trace_paths:
    raw = path.read_bytes()
    print(f"trace={path} sha256={sha256(raw).hexdigest()}")
    for line_number, line in enumerate(raw.decode().splitlines(), 1):
        record = json.loads(line)
        payload = record.get("payload", {})
        if record.get("type") == "response_item":
            subtype = str(payload.get("type", "<missing>"))
            response_types[subtype] += 1
            role = payload.get("role")
            if role:
                roles[str(role)] += 1
            if subtype in ("function_call", "custom_tool_call"):
                function_calls += 1
                function_names[str(payload.get("name", "<missing>"))] += 1
            elif subtype in ("function_call_output", "custom_tool_call_output"):
                function_outputs += 1
            elif subtype == "message" and role == "assistant":
                content = payload.get("content", [])
                text_parts = [
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict) and item.get("type") in ("output_text", "text")
                ]
                assistant_messages.append((line_number, "\n".join(text_parts)))
        elif record.get("type") == "event_msg":
            event_types[str(payload.get("type", "<missing>"))] += 1

print(f"response_item_types={dict(sorted(response_types.items()))}")
print(f"event_message_types={dict(sorted(event_types.items()))}")
print(f"roles={dict(sorted(roles.items()))}")
print(f"function_names={dict(sorted(function_names.items()))}")
print(f"function_calls={function_calls} function_outputs={function_outputs} paired={function_calls == function_outputs}")
print(f"assistant_messages={len(assistant_messages)}")
if assistant_messages:
    line_number, text = assistant_messages[-1]
    print(f"final_assistant_trace_line={line_number}")
    print("final_assistant_message_begin")
    print(text)
    print("final_assistant_message_end")
