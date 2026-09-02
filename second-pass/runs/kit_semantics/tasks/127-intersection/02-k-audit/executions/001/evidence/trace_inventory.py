#!/usr/bin/env python3
import collections
import json
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_calls: list[tuple[int, str, str]] = []
tool_outputs: list[tuple[int, str, str]] = []
assistant_messages: list[tuple[int, str]] = []

with trace.open() as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        top_type = record.get("type", "<missing>")
        top_types[top_type] += 1
        payload = record.get("payload", {})
        if isinstance(payload, dict):
            payload_type = payload.get("type", "<missing>")
            payload_types[f"{top_type}/{payload_type}"] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                name = payload.get("name", "<missing>")
                arguments = payload.get("arguments", payload.get("input", ""))
                tool_calls.append((line_number, name, str(arguments)))
            elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                call_id = payload.get("call_id", "<missing>")
                output = str(payload.get("output", ""))
                tool_outputs.append((line_number, call_id, output))
            elif payload_type == "message" and payload.get("role") == "assistant":
                texts = []
                for item in payload.get("content", []):
                    if isinstance(item, dict) and "text" in item:
                        texts.append(str(item["text"]))
                assistant_messages.append((line_number, "\n".join(texts)))

print(f"trace={trace}")
print(f"parsed_jsonl_records={sum(top_types.values())}")
for key, count in sorted(top_types.items()):
    print(f"top_type[{key}]={count}")
for key, count in sorted(payload_types.items()):
    print(f"payload_type[{key}]={count}")
print(f"tool_calls={len(tool_calls)}")
for line_number, name, arguments in tool_calls:
    compact = arguments.replace("\n", "\\n")
    print(f"TOOL_CALL line={line_number} name={name} arguments={compact[:2000]}")
print(f"tool_outputs={len(tool_outputs)}")
for line_number, call_id, output in tool_outputs:
    compact = output.replace("\n", "\\n")
    print(f"TOOL_OUTPUT line={line_number} call_id={call_id} output={compact[:800]}")
print(f"assistant_messages={len(assistant_messages)}")
for line_number, message in assistant_messages:
    compact = message.replace("\n", "\\n")
    print(f"ASSISTANT_MESSAGE line={line_number} text={compact[:3000]}")
