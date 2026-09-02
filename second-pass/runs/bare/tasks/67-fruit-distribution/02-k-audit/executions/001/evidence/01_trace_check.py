#!/usr/bin/env python3
"""Validate the untrusted JSONL generation trace as a readable evidence artifact."""

import json
from pathlib import Path


trace_paths = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"trace_file_count={len(trace_paths)}")
for path in trace_paths:
    count = 0
    type_counts: dict[str, int] = {}
    first_timestamp = None
    last_timestamp = None
    final_messages: list[str] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            count += 1
            record_type = str(record.get("type"))
            type_counts[record_type] = type_counts.get(record_type, 0) + 1
            timestamp = record.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            payload = record.get("payload", {})
            if (
                record_type == "event_msg"
                and payload.get("type") == "agent_message"
                and payload.get("phase") == "final_answer"
            ):
                final_messages.append(str(payload.get("message")))
    print(f"path={path}")
    print(f"json_records={count}")
    print(f"first_timestamp={first_timestamp}")
    print(f"last_timestamp={last_timestamp}")
    print(f"type_counts={json.dumps(type_counts, sort_keys=True)}")
    print(f"final_message_count={len(final_messages)}")
    for message in final_messages:
        print(f"untrusted_final_message={message!r}")
