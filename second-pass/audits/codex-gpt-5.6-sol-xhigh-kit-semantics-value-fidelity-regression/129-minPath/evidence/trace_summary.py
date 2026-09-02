#!/usr/bin/env python3
"""Read an entire Codex JSONL trace and emit a bounded structural summary."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()

    raw = args.trace.read_bytes()
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    timestamps: list[str] = []
    parse_errors = 0
    final_assistant_messages: list[str] = []

    for line_number, line in enumerate(raw.splitlines(), 1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
            continue
        timestamps.append(str(item.get("timestamp", "")))
        top_types[str(item.get("type", "<missing>"))] += 1
        payload = item.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type", "<missing>"))
        payload_types[payload_type] += 1
        role = payload.get("role")
        if role is not None:
            roles[str(role)] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            tool_names[str(payload.get("name", "<missing>"))] += 1
        if payload_type == "message" and role == "assistant":
            pieces = []
            for content in payload.get("content", []):
                if isinstance(content, dict) and isinstance(content.get("text"), str):
                    pieces.append(content["text"])
            if pieces:
                final_assistant_messages.append("\n".join(pieces))

    print(f"path: {args.trace}")
    print(f"sha256: {hashlib.sha256(raw).hexdigest()}")
    print(f"bytes: {len(raw)}")
    print(f"records: {len(raw.splitlines())}")
    print(f"json parse errors: {parse_errors}")
    print(f"first timestamp: {timestamps[0] if timestamps else '<none>'}")
    print(f"last timestamp: {timestamps[-1] if timestamps else '<none>'}")
    print(f"top-level types: {dict(sorted(top_types.items()))}")
    print(f"payload types: {dict(sorted(payload_types.items()))}")
    print(f"message roles: {dict(sorted(roles.items()))}")
    print(f"tool calls: {dict(sorted(tool_names.items()))}")
    print(f"assistant message count: {len(final_assistant_messages)}")
    if final_assistant_messages:
        bounded = final_assistant_messages[-1].replace("\x00", "")
        print("last assistant message (untrusted claim, bounded):")
        print(bounded[:2000])
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
