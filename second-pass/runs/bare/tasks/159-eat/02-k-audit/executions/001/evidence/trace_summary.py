#!/usr/bin/env python3
"""Summarize provenance claims without trusting or replaying the trace."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


def text_blocks(payload: dict) -> str:
    chunks: list[str] = []
    for item in payload.get("content", []):
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            chunks.append(item["text"])
    return "\n".join(chunks)


trace = Path(sys.argv[1])
rows = [json.loads(line) for line in trace.read_text().splitlines()]
print(f"JSONL_RECORDS={len(rows)}")
print(f"FIRST_TIMESTAMP={rows[0].get('timestamp')}")
print(f"LAST_TIMESTAMP={rows[-1].get('timestamp')}")
print("TOP_TYPES=" + repr(sorted(Counter(row.get("type") for row in rows).items())))

response_types = Counter(
    row.get("payload", {}).get("type")
    for row in rows
    if row.get("type") == "response_item"
)
print("RESPONSE_ITEM_TYPES=" + repr(sorted(response_types.items())))

proof_mentions: list[str] = []
final_messages: list[str] = []
for row in rows:
    payload = row.get("payload", {})
    if row.get("type") == "response_item" and payload.get("type") == "custom_tool_call":
        call = payload.get("input", "")
        if any(word in call for word in ("kompile", "kprove", "krun", "prove.sh")):
            proof_mentions.append(" ".join(call.split())[:500])
    if row.get("type") == "response_item" and payload.get("type") == "message":
        if payload.get("role") == "assistant":
            message = text_blocks(payload)
            if message:
                final_messages.append(message)

print(f"PROOF_RELATED_TOOL_CALLS={len(proof_mentions)}")
for index, call in enumerate(proof_mentions, 1):
    print(f"CALL_{index}={call}")

print(f"ASSISTANT_MESSAGES={len(final_messages)}")
for index, message in enumerate(final_messages, 1):
    print(f"MESSAGE_{index}={' '.join(message.split())[:1000]}")
