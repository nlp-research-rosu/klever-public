#!/usr/bin/env python3
"""Bounded structural inspection of the untrusted generation trace."""

from collections import Counter
import glob
import hashlib
import json
from pathlib import Path


paths = [Path(path) for path in glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True)]
print(f"trace_files={len(paths)}")
for path in sorted(paths):
    data = path.read_bytes()
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    command_summaries: list[str] = []
    agent_messages: list[str] = []
    line_count = 0
    for line_count, line in enumerate(data.decode("utf-8").splitlines(), 1):
        record = json.loads(line)
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload", {})
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if payload_type in {"custom_tool_call", "function_call"}:
            name = str(payload.get("name"))
            tool_names[name] += 1
            text = str(payload.get("input") or payload.get("arguments") or "")
            first_nonempty = next(
                (part.strip() for part in text.splitlines() if part.strip()), ""
            )
            command_summaries.append(
                f"line={line_count} tool={name} first_line={first_nonempty[:240]}"
            )
        if payload_type == "message" and payload.get("role") == "assistant":
            texts = [
                item.get("text", "")
                for item in payload.get("content", [])
                if isinstance(item, dict)
            ]
            if texts:
                agent_messages.append(" ".join(texts))
    print(f"path={path}")
    print(f"sha256={hashlib.sha256(data).hexdigest()}")
    print(f"lines={line_count}")
    print(f"top_types={dict(top_types)}")
    print(f"payload_types={dict(payload_types)}")
    print(f"tool_names={dict(tool_names)}")
    print("custom_call_summaries:")
    for summary in command_summaries:
        print(f"  {summary}")
    print(f"assistant_messages={len(agent_messages)}")
    for index, message in enumerate(agent_messages, 1):
        print(f"  assistant_message_{index}={message[:500]}")
