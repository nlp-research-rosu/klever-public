#!/usr/bin/env python3
"""Validate and summarize the untrusted generation JSONL without executing it."""

from collections import Counter, deque
import json
from pathlib import Path


paths = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
if not paths:
    raise SystemExit("no structured trace")

counts: Counter[str] = Counter()
assistant_texts: deque[str] = deque(maxlen=4)
records = 0

for path in paths:
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            records += 1
            counts[str(record.get("type"))] += 1
            payload = record.get("payload", {})
            if (
                record.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
            ):
                for part in payload.get("content", []):
                    if part.get("type") == "output_text":
                        assistant_texts.append(str(part.get("text", "")))

print(f"trace_json_validation=ok records={records} files={len(paths)}")
for kind, count in sorted(counts.items()):
    print(f"trace_type {kind} {count}")
print("trace_final_assistant_claims")
for text in assistant_texts:
    print(text[-4000:])
