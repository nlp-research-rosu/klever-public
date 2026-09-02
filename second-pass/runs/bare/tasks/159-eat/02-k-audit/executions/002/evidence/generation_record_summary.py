#!/usr/bin/env python3
"""Parse every structured trace record and summarize untrusted generation logs."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence")
trace_files = sorted((root / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
response_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
event_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
commands: list[str] = []
agent_messages: list[str] = []
errors: list[str] = []
malformed: list[str] = []
total = 0

for path in trace_files:
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            total += 1
            try:
                item = json.loads(line)
            except Exception as error:
                malformed.append(f"{path}:{line_number}: {error}")
                continue
            top_type = str(item.get("type"))
            top_types[top_type] += 1
            payload = item.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if top_type == "response_item":
                response_types[payload_type] += 1
                if payload_type in {"custom_tool_call", "function_call"}:
                    name = str(payload.get("name"))
                    tool_names[name] += 1
                    raw_input = payload.get("input", payload.get("arguments", ""))
                    commands.append(
                        f"{path.name}:{line_number} tool={name}\n{raw_input}"
                    )
                if payload_type == "message":
                    roles[str(payload.get("role"))] += 1
            if top_type == "event_msg":
                event_types[payload_type] += 1
                if payload_type == "agent_message":
                    agent_messages.append(str(payload.get("message", "")))
                if payload_type in {"error", "stream_error"}:
                    errors.append(f"{path.name}:{line_number}: {payload}")

print(f"trace_files={len(trace_files)} records={total} malformed={len(malformed)}")
print(f"top_types={dict(top_types)}")
print(f"payload_types={dict(payload_types)}")
print(f"response_types={dict(response_types)}")
print(f"event_types={dict(event_types)}")
print(f"tool_names={dict(tool_names)}")
print(f"message_roles={dict(roles)}")
print(f"error_events={len(errors)}")
for error in errors:
    print(f"ERROR_EVENT {error}")
for bad in malformed:
    print(f"MALFORMED {bad}")

print("FINAL_AGENT_MESSAGES_BEGIN")
for message in agent_messages[-3:]:
    print(message)
print("FINAL_AGENT_MESSAGES_END")

commands_path = Path("/audit-output/evidence/generation_trace_tool_calls.txt")
with commands_path.open("w", encoding="utf-8") as stream:
    stream.write("\n\n".join(commands))
    stream.write("\n")
print(f"tool_calls_written={commands_path} count={len(commands)}")

output_path = root / "codex-output.log"
output_text = output_path.read_text(encoding="utf-8", errors="replace")
needles = [
    "kprove",
    "#Top",
    "WarnStuckClaimState",
    "ERROR",
    "failed",
    "succeeded",
    "RESULT:",
]
print(
    f"codex_output chars={len(output_text)} lines={len(output_text.splitlines())} "
    f"replacement_chars={output_text.count(chr(0xfffd))}"
)
for needle in needles:
    print(f"codex_output occurrences {needle!r}={output_text.count(needle)}")

last_text = (root / "codex-last.txt").read_text(encoding="utf-8")
prompt_text = (root / "prompt.txt").read_text(encoding="utf-8")
print(f"codex_last chars={len(last_text)} lines={len(last_text.splitlines())}")
print(f"prompt chars={len(prompt_text)} lines={len(prompt_text.splitlines())}")
print("codex_last_text_begin")
print(last_text)
print("codex_last_text_end")
