#!/usr/bin/env python3
"""Extract every generated-agent message and tool invocation from the JSONL trace."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T10-11-05-019fae6d-e3ff-7982-88c6-9975887e2be8.jsonl"
)


def main() -> None:
    emitted = 0
    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = payload.get("type")
            if payload_type in {
                "agent_message",
                "message",
                "function_call",
                "custom_tool_call",
                "patch_apply_end",
                "task_complete",
            }:
                emitted += 1
                selected = {
                    key: payload.get(key)
                    for key in (
                        "type",
                        "role",
                        "name",
                        "arguments",
                        "input",
                        "message",
                        "content",
                        "status",
                    )
                    if key in payload
                }
                print(f"TRACE_LINE {line_number}")
                print(json.dumps(selected, sort_keys=True, ensure_ascii=False))
    print(f"TRACE_SUMMARY_COMPLETE emitted={emitted}")


if __name__ == "__main__":
    main()
