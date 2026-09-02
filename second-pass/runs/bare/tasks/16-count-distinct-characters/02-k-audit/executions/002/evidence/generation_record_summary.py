#!/usr/bin/env python3
"""Parse every retained structured-trace record and summarize untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = next(
    Path("/generation-evidence/codex-trace").rglob(
        "rollout-*.jsonl"
    )
)
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
assistant_text = []
records = []
with trace.open(encoding="utf-8") as stream:
    for number, line in enumerate(stream, 1):
        record = json.loads(line)
        records.append(record)
        top_types[record.get("type", "NO_TYPE")] += 1
        payload = record.get("payload") or {}
        payload_types[payload.get("type", "NO_PAYLOAD_TYPE")] += 1
        if payload.get("type") == "message" and payload.get("role") == "assistant":
            for item in payload.get("content", []):
                if isinstance(item, dict) and "text" in item:
                    assistant_text.append((number, item["text"]))

usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)
selected = usage["selected_event"]["line_number"]
assert 1 <= selected <= len(records)

print(f"trace={trace}")
print(f"valid_json_records={len(records)}")
print(f"top_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"usage_selected_event_line={selected}")
print(f"assistant_messages={len(assistant_text)}")
for number, text in assistant_text:
    compact = " ".join(text.split())
    print(f"assistant_line_{number}={compact[:500]}")

output = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
for needle in (
    "kompile verification.k",
    "kprove spec.k",
    "#Top",
    "RESULT: KPROVE_PASSED",
):
    print(f"codex_output_count[{needle!r}]={output.count(needle)}")
print(f"codex_output_lines={len(output.splitlines())}")
print("STRUCTURED TRACE AND TEXT LOG PARSED SUCCESSFULLY")
