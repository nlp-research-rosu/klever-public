#!/usr/bin/env python3
"""Bounded structural inspection of the complete untrusted generation records."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


GEN = Path("/generation-evidence")
trace_files = sorted((GEN / "codex-trace").rglob("*.jsonl"))
tool_names: collections.Counter[str] = collections.Counter()
shell_commands: list[str] = []
final_messages: list[str] = []
line_count = 0
for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            line_count += 1
            event = json.loads(line)
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = payload.get("type")
            if payload_type in {"function_call", "custom_tool_call"}:
                name = str(payload.get("name"))
                tool_names[name] += 1
                args = payload.get("arguments") or payload.get("input")
                if isinstance(args, str) and name in {
                    "exec_command", "container.exec", "functions.exec_command"
                }:
                    try:
                        decoded = json.loads(args)
                    except json.JSONDecodeError:
                        decoded = None
                    if isinstance(decoded, dict) and isinstance(decoded.get("cmd"), str):
                        shell_commands.append(decoded["cmd"])
            if payload_type == "message" and payload.get("role") == "assistant":
                content = payload.get("content")
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "output_text":
                            final_messages.append(str(block.get("text", "")))
            if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                final_messages.append(str(payload.get("message", "")))

output_text = (GEN / "codex-output.log").read_text(errors="replace")
interesting_output_lines = [
    line for line in output_text.splitlines()
    if re.search(r"\b(?:kompile|kprove|krun)\b|#Top|WarnStuckClaimState|RESULT:", line)
]

print("COMMAND: python3 /audit-output/evidence/generation_record_summary.py")
print(f"TRACE_FILES={len(trace_files)}")
print(f"TRACE_JSON_LINES={line_count}")
print("TOOL_CALL_COUNTS=" + json.dumps(dict(sorted(tool_names.items()))))
print(f"SHELL_COMMANDS_EXTRACTED={len(shell_commands)}")
for index, command in enumerate(shell_commands, 1):
    compact = re.sub(r"\s+", " ", command).strip()
    print(f"SHELL_COMMAND_{index:03d}={compact[:1000]}")
print(f"CODEX_OUTPUT_BYTES={len(output_text.encode())}")
print(f"CODEX_OUTPUT_LINES={len(output_text.splitlines())}")
print(f"CODEX_OUTPUT_TOP_COUNT={output_text.count('#Top')}")
print(f"CODEX_OUTPUT_STUCK_COUNT={output_text.count('WarnStuckClaimState')}")
print(f"INTERESTING_OUTPUT_LINE_COUNT={len(interesting_output_lines)}")
for line in interesting_output_lines[-120:]:
    print("OUTPUT_TAIL_MATCH=" + line[:1200])
print(f"FINAL_MESSAGE_RECORDS={len(final_messages)}")
for message in final_messages[-4:]:
    print("FINAL_MESSAGE=" + re.sub(r"\s+", " ", message).strip()[:2000])
print("EXIT_STATUS=0")
