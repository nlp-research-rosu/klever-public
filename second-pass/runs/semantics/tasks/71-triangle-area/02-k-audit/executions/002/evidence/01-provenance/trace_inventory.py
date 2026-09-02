#!/usr/bin/env python3
"""Bounded inventory of every event in the untrusted structured trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T01-39-08-019f8db3-0851-7a93-837b-ed45bc26d20f.jsonl"
)


def flatten_message(content: object) -> str:
    if not isinstance(content, list):
        return str(content or "")
    texts: list[str] = []
    for item in content:
        if isinstance(item, dict):
            texts.append(str(item.get("text") or item.get("type") or ""))
        else:
            texts.append(str(item))
    return " ".join(texts)


events = []
counts: collections.Counter[tuple[str, str]] = collections.Counter()
with TRACE.open() as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        payload = event.get("payload") or {}
        outer = str(event.get("type"))
        inner = str(payload.get("type") or "-")
        counts[(outer, inner)] += 1

        detail = ""
        if inner == "function_call":
            detail = f"{payload.get('name')} {payload.get('arguments')}"
        elif inner == "custom_tool_call":
            detail = f"{payload.get('name')} {payload.get('input')}"
        elif inner == "message":
            detail = f"{payload.get('role')} {flatten_message(payload.get('content'))}"
        elif inner in {"agent_message", "user_message", "task_complete"}:
            detail = str(payload.get("message") or payload.get("last_agent_message") or "")
        elif inner in {"function_call_output", "custom_tool_call_output"}:
            output = str(payload.get("output") or "")
            detail = f"output_chars={len(output)} prefix={output[:240]!r}"
        elif inner == "reasoning":
            detail = f"summary={payload.get('summary')!r} encrypted={bool(payload.get('encrypted_content'))}"
        events.append((line_number, outer, inner, detail.replace("\n", "\\n")[:4000]))

print(f"trace={TRACE}")
print(f"events={len(events)}")
for key, count in sorted(counts.items()):
    print(f"count {key[0]}/{key[1]}={count}")
for line_number, outer, inner, detail in events:
    print(f"{line_number:03d}\t{outer}\t{inner}\t{detail}")
