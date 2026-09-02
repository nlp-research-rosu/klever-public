#!/usr/bin/env python3
"""Read the structured candidate trace as untrusted generation evidence."""

import collections
import json
import pathlib

path = next(pathlib.Path("/candidate/codex-trace").rglob("*.jsonl"))
counts = collections.Counter()
finals = []
for line_number, line in enumerate(path.open(), 1):
    item = json.loads(line)
    counts[item.get("type", "<missing>")] += 1
    payload = item.get("payload", {})
    if payload.get("type") in {"task_complete", "agent_message"}:
        message = payload.get("last_agent_message") or payload.get("message") or ""
        if "#Top" in message or "RESULT:" in message:
            finals.append((line_number, payload.get("type"), message[-700:]))

print("TRACE_PATH:", path)
print("RECORD_COUNTS:", dict(counts))
print("UNTRUSTED_FINAL_CLAIMS:")
for entry in finals:
    print(entry)
