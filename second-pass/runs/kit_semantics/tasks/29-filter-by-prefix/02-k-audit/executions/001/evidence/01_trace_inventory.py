#!/usr/bin/env python3
"""Read every structured generation-trace record and emit a bounded inventory."""

import collections
import json
from pathlib import Path

trace = Path(
    "/generation-evidence/codex-trace/2026/07/24/"
    "rollout-2026-07-24T23-46-28-019f9798-992f-7472-abd1-9a38db7606fd.jsonl"
)
outer = collections.Counter()
payload_types = collections.Counter()
roles = collections.Counter()
commands = []
patches = []
assistant_messages = []
function_outputs = []

with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        outer[record.get("type")] += 1
        payload = record.get("payload", {})
        payload_type = payload.get("type")
        payload_types[payload_type] += 1
        if record.get("type") != "response_item":
            continue
        if payload_type == "message":
            role = payload.get("role", "<none>")
            roles[role] += 1
            if role == "assistant":
                text = "\n".join(
                    part.get("text", "")
                    for part in payload.get("content", [])
                    if part.get("type") in {"input_text", "output_text"}
                )
                assistant_messages.append((line_number, text))
        elif payload_type == "function_call":
            name = payload.get("name", "")
            raw_args = payload.get("arguments", "")
            try:
                args = json.loads(raw_args)
            except (TypeError, json.JSONDecodeError):
                args = {}
            if name in {"exec_command", "functions.exec_command"}:
                commands.append((line_number, args.get("cmd", raw_args)))
            elif name in {"apply_patch", "functions.apply_patch"}:
                patches.append((line_number, raw_args[:500]))
        elif payload_type == "function_call_output":
            output = payload.get("output", "")
            if isinstance(output, str):
                function_outputs.append((line_number, len(output), output[:160]))

print("COMMAND: python3 /audit-output/evidence/01_trace_inventory.py")
print(f"parsed_lines={sum(outer.values())}")
print("outer_types=" + json.dumps(dict(sorted(outer.items())), sort_keys=True))
print("payload_types=" + json.dumps({str(k): v for k, v in sorted(payload_types.items(), key=lambda x: str(x[0]))}))
print("message_roles=" + json.dumps(dict(sorted(roles.items())), sort_keys=True))
print(f"commands={len(commands)} patches={len(patches)} assistant_messages={len(assistant_messages)} function_outputs={len(function_outputs)}")

print("\n== All recorded shell commands (bounded to 1200 characters each) ==")
for line_number, command in commands:
    print(f"TRACE_LINE {line_number}: {command[:1200]}")

print("\n== Patch call prefixes ==")
for line_number, patch in patches:
    print(f"TRACE_LINE {line_number}: {patch}")

print("\n== Assistant message inventory ==")
for line_number, message in assistant_messages:
    compact = " ".join(message.split())
    print(f"TRACE_LINE {line_number} chars={len(message)}: {compact[:500]}")

print("\n== Function-output inventory (prefix only) ==")
for line_number, length, prefix in function_outputs:
    compact = " ".join(prefix.split())
    print(f"TRACE_LINE {line_number} chars={length}: {compact}")

print("SCRIPT_EXIT: 0")
