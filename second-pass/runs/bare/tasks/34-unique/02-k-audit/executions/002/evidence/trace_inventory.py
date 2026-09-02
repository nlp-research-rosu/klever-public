#!/usr/bin/env python3
"""Read every structured generation trace record and emit a bounded inventory."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def clipped(value: object, limit: int = 500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...<clipped>"


def main() -> None:
    paths = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"TRACE_FILES {len(paths)}")
    type_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    parsed = 0
    commands = 0
    outputs = 0
    messages = 0
    for path in paths:
        print(f"TRACE_FILE {path.relative_to(TRACE_ROOT)}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                parsed += 1
                outer_type = str(record.get("type"))
                type_counts[outer_type] += 1
                payload = record.get("payload", {})
                inner_type = str(payload.get("type"))
                payload_counts[f"{outer_type}/{inner_type}"] += 1
                if outer_type == "response_item" and inner_type == "custom_tool_call":
                    commands += 1
                    print(
                        f"CALL line={line_number} name={payload.get('name')} "
                        f"args={clipped(payload.get('arguments'), 1200)}"
                    )
                elif (
                    outer_type == "response_item"
                    and inner_type == "custom_tool_call_output"
                ):
                    outputs += 1
                    print(
                        f"CALL_OUTPUT line={line_number} "
                        f"output={clipped(payload.get('output'), 1200)}"
                    )
                elif outer_type == "event_msg" and inner_type in {
                    "agent_message",
                    "task_complete",
                }:
                    messages += 1
                    print(
                        f"EVENT line={line_number} type={inner_type} "
                        f"payload={clipped(payload, 1200)}"
                    )
                elif outer_type == "response_item" and inner_type == "message":
                    role = payload.get("role")
                    if role == "assistant":
                        messages += 1
                        print(
                            f"MESSAGE line={line_number} role={role} "
                            f"content={clipped(payload.get('content'), 1200)}"
                        )
    print(f"PARSED_RECORDS {parsed}")
    print(f"CALLS {commands}")
    print(f"CALL_OUTPUTS {outputs}")
    print(f"SELECTED_MESSAGES {messages}")
    print("TYPE_COUNTS " + json.dumps(type_counts, sort_keys=True))
    print("PAYLOAD_TYPE_COUNTS " + json.dumps(payload_counts, sort_keys=True))


if __name__ == "__main__":
    main()
