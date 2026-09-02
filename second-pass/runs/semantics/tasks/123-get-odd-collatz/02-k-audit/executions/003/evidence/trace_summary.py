#!/usr/bin/env python3
"""Read every structured generation trace event and summarize untrusted claims."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def output_exit_status(output: object) -> str:
    match = re.search(r"(?:Process exited with code|exit_code[\"': ]+)(-?[0-9]+)", str(output))
    return match.group(1) if match else "not-recorded"


outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
pending_calls: dict[str, tuple[str, str]] = {}
completed_tools: list[tuple[str, str, str, int]] = []
messages: list[tuple[str, str]] = []
line_count = 0

for trace_path in sorted(TRACE_ROOT.rglob("*.jsonl")):
    print(f"TRACE_FILE {trace_path}")
    for line_number, raw_line in enumerate(trace_path.read_text().splitlines(), 1):
        line_count += 1
        record = json.loads(raw_line)
        outer = str(record.get("type"))
        outer_types[outer] += 1
        payload = record.get("payload") or {}
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1

        if payload_type in {"function_call", "custom_tool_call"}:
            name = str(payload.get("name"))
            tool_names[name] += 1
            call_id = str(payload.get("call_id"))
            arguments = payload.get("arguments")
            if arguments is None:
                arguments = payload.get("input")
            pending_calls[call_id] = (name, str(arguments))
        elif payload_type in {"function_call_output", "custom_tool_call_output"}:
            call_id = str(payload.get("call_id"))
            name, arguments = pending_calls.pop(
                call_id, ("<unmatched-output>", "<unmatched-output>")
            )
            completed_tools.append(
                (name, arguments, output_exit_status(payload.get("output")), line_number)
            )
        elif payload_type in {"agent_message", "message"}:
            role = str(payload.get("role", payload_type))
            content = payload.get("message", payload.get("content"))
            if role == "assistant" or payload_type == "agent_message":
                messages.append((role, str(content)))

print(f"TOTAL_JSONL_LINES {line_count}")
print(f"OUTER_TYPES {dict(sorted(outer_types.items()))}")
print(f"PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
print(f"TOOL_NAMES {dict(sorted(tool_names.items()))}")
print(f"UNMATCHED_CALLS {sorted(pending_calls)}")
print("COMPLETED_TOOL_CALLS")
for index, (name, arguments, status, line_number) in enumerate(completed_tools, 1):
    compact = " ".join(arguments.split())
    if len(compact) > 2000:
        argument_hash = hashlib.sha256(arguments.encode()).hexdigest()
        compact = (
            compact[:2000]
            + f" ... [truncated; full-argument-sha256={argument_hash}]"
        )
    print(
        f"{index:03d} trace_line={line_number} tool={name} "
        f"recorded_exit={status} args={compact}"
    )
print("ASSISTANT_MESSAGES")
for index, (role, message) in enumerate(messages, 1):
    compact = " ".join(message.split())
    print(f"{index:03d} role={role} text={compact}")
