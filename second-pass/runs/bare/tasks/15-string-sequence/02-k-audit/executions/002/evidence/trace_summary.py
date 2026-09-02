#!/usr/bin/env python3
"""Parse every launcher-retained generation trace event and summarize actions."""

from __future__ import annotations

import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 600) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[:limit] + "...[bounded]"
    return text


print("COMMAND: python3 /audit-output/evidence/trace_summary.py")
files = sorted(TRACE_ROOT.rglob("*"))
regular_files = [path for path in files if path.is_file() and not path.is_symlink()]
print(f"trace_regular_files={len(regular_files)}")
line_total = 0
for path in regular_files:
    relative = path.relative_to(TRACE_ROOT)
    print(f"FILE {relative}")
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            line_total += 1
            event = json.loads(line)
            event_type = event.get("type")
            payload = event.get("payload", {})
            subtype = payload.get("type") if isinstance(payload, dict) else None
            fields = [
                f"LINE={line_number}",
                f"timestamp={event.get('timestamp')}",
                f"type={event_type}",
                f"subtype={subtype}",
            ]
            if event_type == "response_item" and isinstance(payload, dict):
                fields.append(f"role={payload.get('role')}")
                fields.append(f"name={payload.get('name')}")
                if subtype == "function_call":
                    fields.append(f"arguments={compact(payload.get('arguments'))}")
                elif subtype == "function_call_output":
                    fields.append(f"output={compact(payload.get('output'))}")
                elif subtype == "custom_tool_call":
                    fields.append(f"input={compact(payload.get('input'))}")
                elif subtype == "custom_tool_call_output":
                    fields.append(f"output={compact(payload.get('output'))}")
                elif subtype == "message":
                    fields.append(f"content={compact(payload.get('content'))}")
            elif event_type == "event_msg" and isinstance(payload, dict):
                useful = {
                    key: payload.get(key)
                    for key in (
                        "message",
                        "last_agent_message",
                        "reason",
                        "turn_id",
                        "status",
                    )
                    if key in payload
                }
                fields.append(f"payload={compact(useful)}")
            print("|".join(fields))
print(f"parsed_lines={line_total}")
print("SCRIPT_EXIT=0")
