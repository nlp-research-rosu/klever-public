#!/usr/bin/env python3
"""Read and structurally summarize the complete untrusted generation trace."""

from collections import Counter
import json
from pathlib import Path

trace_files = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"trace_file_count={len(trace_files)}")
for path in trace_files:
    outer_types = Counter()
    payload_types = Counter()
    malformed = []
    final_messages = []
    line_count = 0
    for line_count, line in enumerate(
        path.open("r", encoding="utf-8"), start=1
    ):
        try:
            record = json.loads(line)
        except Exception as error:
            malformed.append((line_count, type(error).__name__, str(error)))
            continue
        outer_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if payload.get("type") in {"agent_message", "task_complete"}:
                message = payload.get("message") or payload.get("last_agent_message")
                if isinstance(message, str):
                    final_messages.append(message)
    print(f"file={path}")
    print(f"bytes={path.stat().st_size}")
    print(f"lines={line_count}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"malformed_count={len(malformed)}")
    for item in malformed[:20]:
        print(f"MALFORMED={item!r}")
    print(f"final_message_count={len(final_messages)}")
    for message in final_messages[-3:]:
        print(f"FINAL_CLAIM={message!r}")
