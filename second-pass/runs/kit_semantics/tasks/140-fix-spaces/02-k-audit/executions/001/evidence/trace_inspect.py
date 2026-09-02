#!/usr/bin/env python3
"""Parse every structured Codex trace record and summarize auditable actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def clipped(value: object, limit: int = 500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...<clipped>"


def main() -> int:
    files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"trace_files={len(files)}")
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    records = 0
    for path in files:
        print(f"TRACE {path.relative_to(TRACE_ROOT)}")
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                records += 1
                outer = str(record.get("type"))
                outer_types[outer] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type"))
                    payload_types[payload_type] += 1
                else:
                    payload_type = ""

                if outer == "response_item" and isinstance(payload, dict):
                    if payload_type in {
                        "function_call",
                        "custom_tool_call",
                        "local_shell_call",
                        "message",
                    }:
                        role = payload.get("role", "")
                        if payload_type == "message" and role not in {"assistant", "user"}:
                            continue
                        fields = {
                            key: payload[key]
                            for key in ("name", "arguments", "command", "role", "status")
                            if key in payload
                        }
                        if payload_type == "message":
                            fields["content"] = payload.get("content")
                        print(
                            f"{line_number}: response_item/{payload_type} "
                            f"{clipped(fields, 1200)}"
                        )
                elif outer == "event_msg" and isinstance(payload, dict):
                    if payload_type in {
                        "agent_message",
                        "task_complete",
                        "task_completed",
                        "token_count",
                    }:
                        fields = {
                            key: payload[key]
                            for key in (
                                "message",
                                "last_agent_message",
                                "input_tokens",
                                "output_tokens",
                                "total_tokens",
                            )
                            if key in payload
                        }
                        print(
                            f"{line_number}: event_msg/{payload_type} "
                            f"{clipped(fields, 1200)}"
                        )
    print(f"records_parsed={records}")
    print(f"outer_type_counts={dict(sorted(outer_types.items()))}")
    print(f"payload_type_counts={dict(sorted(payload_types.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
