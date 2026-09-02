#!/usr/bin/env python3
"""Read and summarize every event in the untrusted generation records."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


ROOT = Path("/generation-evidence")
trace_files = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
calls: dict[str, tuple[str, str]] = {}
call_rows: list[str] = []
agent_messages: list[str] = []

line_count = 0
for trace_file in trace_files:
    for line_number, line in enumerate(trace_file.read_text().splitlines(), 1):
        line_count += 1
        event = json.loads(line)
        top_types[str(event.get("type"))] += 1
        payload = event.get("payload") or {}
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            call_id = str(payload.get("call_id"))
            name = str(payload.get("name"))
            arguments = str(payload.get("arguments") or "")
            calls[call_id] = (name, arguments)
        elif payload_type in {"function_call_output", "custom_tool_call_output"}:
            call_id = str(payload.get("call_id"))
            name, arguments = calls.get(call_id, ("UNKNOWN", ""))
            output = str(payload.get("output") or "")
            command = ""
            if arguments:
                try:
                    decoded = json.loads(arguments)
                    command = str(decoded.get("cmd") or decoded)
                except (ValueError, AttributeError):
                    command = arguments
            exit_matches = re.findall(
                r"(?:Process exited with code|exit_code[\"']?\s*[:=]|Exit code:)\s*(\d+)",
                output,
            )
            status = exit_matches[-1] if exit_matches else "not-explicit"
            signals = []
            if "#Top" in output:
                signals.append("#Top")
            if "WarnStuckClaimState" in output:
                signals.append("stuck")
            if "timed out" in output.lower() or "code 124" in output:
                signals.append("timeout")
            first_command_line = command.splitlines()[0][:240] if command else ""
            call_rows.append(
                f"{len(call_rows) + 1:03d} {name} status={status} "
                f"signals={','.join(signals) or 'none'} command={first_command_line}"
            )
        elif payload_type in {"message", "agent_message"}:
            content = payload.get("content")
            text = ""
            if isinstance(content, list):
                text = " ".join(
                    str(item.get("text", ""))
                    for item in content
                    if isinstance(item, dict)
                )
            elif content is not None:
                text = str(content)
            if text:
                agent_messages.append(text)

output_log = (ROOT / "codex-output.log").read_text()
last_text = (ROOT / "codex-last.txt").read_text()
prompt_text = (ROOT / "prompt.txt").read_text()

print(f"trace_files={[str(path) for path in trace_files]}")
print(f"trace_json_line_count={line_count}")
print(f"trace_top_types={dict(top_types)}")
print(f"trace_payload_types={dict(payload_types)}")
print(f"completed_tool_output_count={len(call_rows)}")
for row in call_rows:
    print(row)
print(f"agent_message_count={len(agent_messages)}")
for index, message in enumerate(agent_messages, 1):
    print(f"AGENT_MESSAGE_{index}: {message[:1000]}")
print(f"codex_output_chars={len(output_log)} lines={len(output_log.splitlines())}")
for pattern in (
    "#Top",
    "WarnStuckClaimState",
    "Process exited with code 0",
    "Process exited with code 1",
    "Process exited with code 124",
    "RESULT: KPROVE_PASSED",
):
    print(f"codex_output_pattern={pattern!r} count={output_log.count(pattern)}")
print(f"prompt_chars={len(prompt_text)} lines={len(prompt_text.splitlines())}")
print(f"codex_last_chars={len(last_text)}")
print("CODEX_LAST_BEGIN")
print(last_text.rstrip())
print("CODEX_LAST_END")
