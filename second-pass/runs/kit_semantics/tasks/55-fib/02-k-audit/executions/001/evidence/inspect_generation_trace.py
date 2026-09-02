#!/usr/bin/env python3
"""Read every structured trace record and summarize proof-relevant activity."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-33-05-019f97c3-469d-7251-8033-63f5e2afbbd4.jsonl"
)


def walk(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


counts: collections.Counter[str] = collections.Counter()
tool_counts: collections.Counter[str] = collections.Counter()
proof_mentions = []
final_messages = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        counts[record.get("type", "<missing>")] += 1
        payload = record.get("payload", {})
        if isinstance(payload, dict):
            payload_type = payload.get("type")
            if payload_type in {"function_call", "custom_tool_call"}:
                tool_counts[str(payload.get("name", payload_type))] += 1
            if payload_type == "message" and payload.get("role") == "assistant":
                text = json.dumps(payload.get("content", ""), ensure_ascii=False)
                if "RESULT: KPROVE_PASSED" in text:
                    final_messages.append((line_number, text[:800]))
        serialized = json.dumps(record, ensure_ascii=False)
        if any(
            needle in serialized
            for needle in (
                "kompile --backend",
                "kprove spec",
                "WarnStuckClaimState",
                '"#Top',
            )
        ):
            proof_mentions.append((line_number, serialized[:1200]))

print(f"trace={TRACE}")
print(f"records={sum(counts.values())}")
print("record_types=" + json.dumps(dict(sorted(counts.items())), sort_keys=True))
print("tool_calls=" + json.dumps(dict(sorted(tool_counts.items())), sort_keys=True))
print(f"proof_relevant_records={len(proof_mentions)}")
for line_number, text in proof_mentions:
    print(f"TRACE_LINE {line_number}: {text}")
print(f"final_marker_records={len(final_messages)}")
for line_number, text in final_messages:
    print(f"FINAL_LINE {line_number}: {text}")
