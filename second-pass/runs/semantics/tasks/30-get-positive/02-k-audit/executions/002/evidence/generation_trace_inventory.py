#!/usr/bin/env python3
"""Read every structured generation-trace record and inventory its actions."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


def main() -> None:
    trace_root = Path("/generation-evidence/codex-trace")
    traces = sorted(trace_root.rglob("*.jsonl"))
    if not traces:
        raise SystemExit("no structured trace found")

    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    assistant_messages: list[tuple[str, str]] = []
    calls: list[tuple[int, str, str]] = []
    total = 0

    for trace in traces:
        print(
            f"TRACE_FILE {trace.relative_to(trace_root)} "
            f"sha256={hashlib.sha256(trace.read_bytes()).hexdigest()}"
        )
        for line_number, line in enumerate(
            trace.read_text(encoding="utf-8").splitlines(), 1
        ):
            record = json.loads(line)
            total += 1
            top_type = str(record.get("type", "<none>"))
            top_types[top_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<none>"))
                payload_types[payload_type] += 1
                if top_type == "event_msg" and payload_type == "agent_message":
                    assistant_messages.append(
                        (str(payload.get("phase")), str(payload.get("message")))
                    )
                if top_type == "response_item" and payload_type == "function_call":
                    arguments = str(payload.get("arguments", ""))
                    calls.append(
                        (line_number, str(payload.get("name")), arguments)
                    )

    print(f"TRACE_RECORDS {total}")
    print(f"TOP_LEVEL_TYPES {dict(sorted(top_types.items()))}")
    print(f"PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    print(f"ASSISTANT_MESSAGES {len(assistant_messages)}")
    for phase, message in assistant_messages:
        print(f"MESSAGE phase={phase} text={json.dumps(message)}")
    print(f"FUNCTION_CALLS {len(calls)}")
    for line_number, name, arguments in calls:
        print(
            f"CALL line={line_number} name={name} "
            f"arguments={arguments}"
        )
    print("GENERATION_TRACE_FULL_PARSE_OK")


if __name__ == "__main__":
    main()
