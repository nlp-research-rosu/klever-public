#!/usr/bin/env python3
"""Parse every structured generation-trace event and summarize untrusted claims."""

import collections
import json
from pathlib import Path


trace_path = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T08-22-56-019f8f24-b7d4-73f3-8cab-481aed17f1e2.jsonl"
)
events = []
with trace_path.open() as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        events.append(event)

types = collections.Counter(event.get("type") for event in events)
payload_types = collections.Counter(
    event.get("payload", {}).get("type")
    for event in events
    if isinstance(event.get("payload"), dict) and event["payload"].get("type")
)
print(f"jsonl_valid=True lines={len(events)}")
print(f"event_types={dict(sorted(types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"first_type={events[0].get('type')} last_type={events[-1].get('type')}")

output = Path("/generation-evidence/codex-output.log").read_text(errors="replace")
for needle in ["kprove", "#Top", "WarnStuckClaimState", "RESULT: KPROVE_PASSED", "1000-case"]:
    print(f"codex_output_count[{needle!r}]={output.count(needle)}")
