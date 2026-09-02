#!/usr/bin/env python3
"""Read every structured trace record and summarize untrusted generation actions."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def clipped(value: object, limit: int = 500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...<clipped>"


def main() -> None:
    root = Path("/generation-evidence/codex-trace")
    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    calls: list[tuple[int, str, str, str]] = []
    outputs: list[tuple[int, str, str]] = []
    messages: list[tuple[int, str, str]] = []
    records = 0
    for path in sorted(root.rglob("*.jsonl")):
        print(f"TRACE_FILE {path}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                record = json.loads(line)
                records += 1
                outer = str(record.get("type"))
                payload = record.get("payload", {})
                payload_type = str(payload.get("type")) if isinstance(payload, dict) else type(payload).__name__
                outer_types[outer] += 1
                payload_types[payload_type] += 1
                if isinstance(payload, dict) and payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name"))
                    call_id = str(payload.get("call_id", payload.get("id", "")))
                    args = payload.get("arguments", payload.get("input", ""))
                    calls.append((line_number, name, call_id, clipped(args, 1600)))
                if isinstance(payload, dict) and payload_type in {"function_call_output", "custom_tool_call_output"}:
                    call_id = str(payload.get("call_id", ""))
                    outputs.append((line_number, call_id, clipped(payload.get("output", ""), 1200)))
                if isinstance(payload, dict) and payload_type == "message":
                    role = str(payload.get("role"))
                    messages.append((line_number, role, clipped(payload.get("content", ""), 1200)))
                if isinstance(payload, dict) and payload_type == "agent_message":
                    messages.append((line_number, "agent_message", clipped(payload.get("message", ""), 1200)))
    print(f"TOTAL_RECORDS {records}")
    print(f"OUTER_TYPES {dict(sorted(outer_types.items()))}")
    print(f"PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    print(f"TOOL_CALL_COUNT {len(calls)}")
    for item in calls:
        print(f"TOOL_CALL line={item[0]} name={item[1]} id={item[2]} args={item[3]}")
    print(f"TOOL_OUTPUT_COUNT {len(outputs)}")
    for item in outputs:
        print(f"TOOL_OUTPUT line={item[0]} id={item[1]} output={item[2]}")
    print(f"MESSAGE_COUNT {len(messages)}")
    for item in messages:
        print(f"MESSAGE line={item[0]} role={item[1]} content={item[2]}")


if __name__ == "__main__":
    main()
