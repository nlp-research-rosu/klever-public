#!/usr/bin/env python3
"""Extract an audit-oriented, bounded view of the untrusted generation trace."""

from __future__ import annotations

import json
from pathlib import Path


TRACE_ROOT = Path("/candidate/codex-trace")
MAX_OUTPUT_CHARS = 4000


def text_blocks(value: object) -> str:
    if not isinstance(value, list):
        return repr(value)
    blocks: list[str] = []
    for item in value:
        if isinstance(item, dict) and "text" in item:
            blocks.append(str(item["text"]))
        else:
            blocks.append(repr(item))
    return "\n".join(blocks)


for path in sorted(TRACE_ROOT.rglob("*.jsonl")):
    print(f"TRACE: {path}")
    with path.open(encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, 1):
            record = json.loads(raw)
            payload = record.get("payload", {})
            payload_type = payload.get("type")

            if record.get("type") == "session_meta":
                print(f"[{lineno}] session_meta: {payload}")
            elif payload_type == "agent_message":
                print(f"[{lineno}] agent_message/{payload.get('phase')}:")
                print(payload.get("message", ""))
            elif record.get("type") == "response_item" and payload_type == "custom_tool_call":
                print(f"[{lineno}] tool_call {payload.get('name')}:")
                print(payload.get("input", ""))
            elif record.get("type") == "response_item" and payload_type == "custom_tool_call_output":
                rendered = text_blocks(payload.get("output", []))
                if len(rendered) > MAX_OUTPUT_CHARS:
                    head = rendered[: MAX_OUTPUT_CHARS // 2]
                    tail = rendered[-MAX_OUTPUT_CHARS // 2 :]
                    rendered = (
                        head
                        + f"\n... <{len(rendered) - MAX_OUTPUT_CHARS} chars omitted> ...\n"
                        + tail
                    )
                print(f"[{lineno}] tool_output {payload.get('call_id')}:")
                print(rendered)
            elif payload_type == "task_complete":
                print(f"[{lineno}] task_complete: {payload}")
