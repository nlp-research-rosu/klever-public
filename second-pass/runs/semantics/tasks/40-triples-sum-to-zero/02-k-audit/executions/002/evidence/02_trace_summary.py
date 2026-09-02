#!/usr/bin/env python3
"""Summarize every tool call in the untrusted generation trace without trusting it."""

from __future__ import annotations

import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def bounded(value: object, limit: int = 1800) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return text[:900] + "\n...<bounded>...\n" + text[-900:]


def main() -> None:
    calls: dict[str, dict] = {}
    output_count = 0
    for path in sorted(TRACE_ROOT.rglob("*.jsonl")):
        print(f"TRACE_FILE {path.relative_to(TRACE_ROOT)}")
        with path.open() as stream:
            for line_no, raw in enumerate(stream, 1):
                record = json.loads(raw)
                payload = record.get("payload", {})
                if record.get("type") == "response_item" and payload.get("type") in {
                    "function_call",
                    "custom_tool_call",
                }:
                    call_id = payload.get("call_id", payload.get("id", f"line-{line_no}"))
                    calls[str(call_id)] = payload
                    print(
                        f"\nCALL line={line_no} id={call_id} "
                        f"name={payload.get('name', payload.get('tool_name'))}"
                    )
                    print(bounded(payload.get("arguments", payload.get("input", ""))))
                elif record.get("type") == "response_item" and payload.get("type") in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    call_id = payload.get("call_id", payload.get("id", f"line-{line_no}"))
                    output_count += 1
                    print(f"OUTPUT line={line_no} id={call_id}")
                    print(bounded(payload.get("output", "")))
                elif (
                    record.get("type") == "event_msg"
                    and payload.get("type") in {"agent_message", "task_complete"}
                ):
                    print(f"\nMESSAGE line={line_no} phase={payload.get('phase')}")
                    print(bounded(payload.get("message", payload.get("last_agent_message", ""))))
    print(f"\nSUMMARY calls={len(calls)} outputs={output_count}")


if __name__ == "__main__":
    main()
