#!/usr/bin/env python3
"""Parse every generation trace record and print a bounded semantic inventory."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 1200) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    rendered = rendered.replace("\n", "\\n")
    if len(rendered) > limit:
        return rendered[:limit] + f"...[truncated {len(rendered) - limit} chars]"
    return rendered


records = Counter()
payloads = Counter()
files = sorted(TRACE_ROOT.rglob("*"))
regular_files = [path for path in files if path.is_file() and not path.is_symlink()]

print(f"trace_files={len(regular_files)}")
for path in regular_files:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"FILE {path.relative_to(TRACE_ROOT)} sha256={digest}")
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            record = json.loads(line)
            record_type = record.get("type", "<missing>")
            payload = record.get("payload", {})
            payload_type = payload.get("type", "<missing>")
            records[record_type] += 1
            payloads[(record_type, payload_type)] += 1

            if record_type == "response_item":
                if payload_type == "custom_tool_call":
                    print(
                        f"L{line_number} CALL {payload.get('name')} "
                        f"id={payload.get('call_id')} input={compact(payload.get('input'))}"
                    )
                elif payload_type == "custom_tool_call_output":
                    print(
                        f"L{line_number} OUTPUT id={payload.get('call_id')} "
                        f"value={compact(payload.get('output'))}"
                    )
                elif payload_type == "message":
                    role = payload.get("role")
                    if role in {"user", "assistant"}:
                        print(
                            f"L{line_number} MESSAGE role={role} "
                            f"content={compact(payload.get('content'))}"
                        )
            elif record_type == "event_msg" and payload_type in {
                "agent_message",
                "task_complete",
                "task_started",
            }:
                print(
                    f"L{line_number} EVENT {payload_type} "
                    f"value={compact(payload)}"
                )

print("RECORD_COUNTS")
for key, value in sorted(records.items()):
    print(f"{key}={value}")
print("PAYLOAD_COUNTS")
for (record_type, payload_type), value in sorted(payloads.items()):
    print(f"{record_type}/{payload_type}={value}")
