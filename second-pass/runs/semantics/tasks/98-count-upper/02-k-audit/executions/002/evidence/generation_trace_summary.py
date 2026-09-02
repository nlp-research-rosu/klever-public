#!/usr/bin/env python3
"""Read the complete untrusted generation trace and emit a bounded audit view."""

from __future__ import annotations

import json
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
files = sorted(path for path in root.rglob("*") if path.is_file())

for path in files:
    print(f"TRACE_FILE {path.relative_to(root)}")
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            event = json.loads(line)
            event_type = event.get("type")
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = payload.get("type")
            if event_type == "response_item" and payload_type in {
                "function_call",
                "custom_tool_call",
            }:
                name = payload.get("name", payload.get("tool_name", "<unknown>"))
                arguments = payload.get("arguments", payload.get("input", ""))
                if not isinstance(arguments, str):
                    arguments = json.dumps(arguments, sort_keys=True)
                arguments = arguments.replace("\x00", "<NUL>")
                if len(arguments) > 1200:
                    arguments = arguments[:1200] + "...<truncated>"
                print(f"line={line_no} CALL {name}: {arguments}")
            elif event_type == "response_item" and payload_type in {
                "function_call_output",
                "custom_tool_call_output",
            }:
                output = payload.get("output", "")
                if not isinstance(output, str):
                    output = json.dumps(output, sort_keys=True)
                # The full trace was parsed; bound only the displayed evidence.
                normalized = output.replace("\r", "").replace("\x00", "<NUL>")
                first = normalized[:500].replace("\n", "\\n")
                print(
                    f"line={line_no} OUTPUT bytes={len(output.encode())}: "
                    f"{first}{'...<truncated>' if len(normalized) > 500 else ''}"
                )
            elif event_type in {"event_msg", "response_item"} and payload_type in {
                "agent_message",
                "message",
                "task_complete",
            }:
                text = payload.get("message", payload.get("text", payload.get("content", "")))
                if not isinstance(text, str):
                    text = json.dumps(text, sort_keys=True)
                normalized = text.replace("\r", "").replace("\n", "\\n")
                print(
                    f"line={line_no} MESSAGE bytes={len(text.encode())}: "
                    f"{normalized[:700]}{'...<truncated>' if len(normalized) > 700 else ''}"
                )
