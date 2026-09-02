#!/usr/bin/env python3
import collections
import json
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
files = sorted(root.rglob("*.jsonl"))
top_types = collections.Counter()
payload_types = collections.Counter()
invalid = []
events = 0
commands = []
assistant_finals = []

for path in files:
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            events += 1
            try:
                obj = json.loads(line)
            except Exception as err:
                invalid.append((str(path), line_no, str(err)))
                continue
            top_types[obj.get("type", "<missing>")] += 1
            payload = obj.get("payload")
            if isinstance(payload, dict):
                payload_types[payload.get("type", "<missing>")] += 1
                if payload.get("type") == "function_call":
                    commands.append(
                        (
                            path.name,
                            line_no,
                            payload.get("name"),
                            payload.get("arguments"),
                        )
                    )
                if payload.get("type") == "message" and payload.get("role") == "assistant":
                    content = payload.get("content", [])
                    text_parts = [
                        item.get("text", "")
                        for item in content
                        if isinstance(item, dict) and item.get("type") in {"output_text", "text"}
                    ]
                    if text_parts:
                        assistant_finals.append((path.name, line_no, "\n".join(text_parts)))

print(f"FILES: {[str(path) for path in files]}")
print(f"EVENTS: {events}")
print(f"INVALID_JSON_LINES: {invalid}")
print(f"TOP_LEVEL_TYPES: {dict(sorted(top_types.items()))}")
print(f"PAYLOAD_TYPES: {dict(sorted(payload_types.items()))}")
print(f"FUNCTION_CALL_COUNT: {len(commands)}")
for row in commands[-25:]:
    print(f"FUNCTION_CALL: {row}")
print(f"ASSISTANT_MESSAGE_COUNT: {len(assistant_finals)}")
for path, line_no, message in assistant_finals[-5:]:
    print(f"ASSISTANT_MESSAGE {path}:{line_no}:")
    print(message[:4000])
