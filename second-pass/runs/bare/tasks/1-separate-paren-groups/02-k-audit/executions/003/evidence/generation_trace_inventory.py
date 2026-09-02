#!/usr/bin/env python3
"""Bounded structural inventory of the untrusted generation trace."""

import json
from collections import Counter
from pathlib import Path

path = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T03-47-50-019f8902-81a0-7132-bf36-6f07efd73d96.jsonl"
)
rows = [json.loads(line) for line in path.open()]

print(f"jsonl_events={len(rows)}")
counts = Counter(
    (row.get("type"), row.get("payload", {}).get("type", "-")) for row in rows
)
for (top, payload), count in sorted(counts.items()):
    print(f"event_count={count} top={top} payload={payload}")

roles = Counter(
    row["payload"].get("role")
    for row in rows
    if row.get("type") == "response_item"
    and row.get("payload", {}).get("type") == "message"
)
print(f"message_roles={dict(sorted(roles.items()))}")

assistant_texts: list[str] = []
for row in rows:
    payload = row.get("payload", {})
    if (
        row.get("type") == "response_item"
        and payload.get("type") == "message"
        and payload.get("role") == "assistant"
    ):
        text = " ".join(
            item.get("text", "")
            for item in payload.get("content", [])
            if isinstance(item, dict)
        )
        assistant_texts.append(" ".join(text.split()))

print(f"assistant_messages={len(assistant_texts)}")
print(f"final_assistant_message={assistant_texts[-1]}")
