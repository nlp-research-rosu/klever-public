#!/usr/bin/env python3
"""Structural inspection of the untrusted generation trace and text log."""

from collections import Counter
import json
from pathlib import Path


trace = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T11-33-15-019faeb9-1e01-7b50-b285-1e2fbaf855cb.jsonl"
)
output_log = Path("/generation-evidence/codex-output.log")

events = []
with trace.open() as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        events.append((line_number, event))

type_counts = Counter(event["type"] for _, event in events)
payload_type_counts = Counter(
    event.get("payload", {}).get("type", "<none>")
    for _, event in events
)

tool_calls = []
for line_number, event in events:
    payload = event.get("payload", {})
    if payload.get("type") == "custom_tool_call":
        raw = payload.get("input", "")
        tool_calls.append((line_number, payload.get("name"), raw))

interesting = []
needles = (
    "kompile",
    "kprove",
    "krun",
    "verification.k",
    "spec.k",
    "differential",
    "mutation",
)
for line_number, name, raw in tool_calls:
    if any(needle in raw for needle in needles):
        compact = " ".join(raw.split())
        interesting.append((line_number, name, compact[:500]))

text = output_log.read_text(errors="replace")

print(f"TRACE={trace}")
print(f"TRACE_LINES={len(events)}")
print("TRACE_TYPES=" + json.dumps(type_counts, sort_keys=True))
print("PAYLOAD_TYPES=" + json.dumps(payload_type_counts, sort_keys=True))
print(f"CUSTOM_TOOL_CALLS={len(tool_calls)}")
print(f"INTERESTING_TOOL_CALLS={len(interesting)}")
for item in interesting:
    print("INTERESTING", item)
print(f"CODEX_OUTPUT_BYTES={len(text.encode())}")
print(f"CODEX_OUTPUT_LINES={len(text.splitlines())}")
for needle in ("#Top", "WarnStuckClaimState", "VALIDATED", "RESULT:"):
    print(f"CODEX_OUTPUT_COUNT {needle!r} {text.count(needle)}")
print(
    "FINAL_TRACE_EVENT="
    + json.dumps(events[-1][1], sort_keys=True)[:1000]
)
