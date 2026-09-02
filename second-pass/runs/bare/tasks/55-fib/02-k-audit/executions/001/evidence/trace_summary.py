#!/usr/bin/env python3
"""Bounded summary of the untrusted structured generation trace."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-11-27-019f894f-0f4b-7912-adc3-c85b88e6a8cd.jsonl"
)


def content_text(payload: dict) -> str:
    texts = []
    for item in payload.get("content", []):
        if not isinstance(item, dict):
            continue
        for field in ("text", "input_text", "output_text"):
            value = item.get(field)
            if isinstance(value, str):
                texts.append(value)
                break
    return "\n".join(texts)


def main() -> None:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    message_roles: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    final_messages: list[str] = []
    command_samples: list[str] = []
    line_count = 0

    digest = hashlib.sha256()
    with TRACE.open("rb") as raw:
        for raw_line in raw:
            digest.update(raw_line)
            line_count += 1
            record = json.loads(raw_line)
            top_types[record.get("type", "(none)")] += 1
            payload = record.get("payload", {})
            if not isinstance(payload, dict):
                continue
            payload_type = payload.get("type", "(none)")
            payload_types[payload_type] += 1
            if payload_type == "message":
                role = payload.get("role", "(none)")
                message_roles[role] += 1
                text = content_text(payload)
                if role == "assistant" and text:
                    final_messages.append(text)
            if payload_type in ("function_call", "custom_tool_call"):
                name = payload.get("name", "(unnamed)")
                tool_names[name] += 1
                arguments = payload.get("arguments") or payload.get("input")
                if isinstance(arguments, str) and len(command_samples) < 20:
                    command_samples.append(arguments[:500].replace("\n", "\\n"))

    print(f"trace={TRACE}")
    print(f"bytes={TRACE.stat().st_size} lines={line_count}")
    print(f"sha256={digest.hexdigest()}")
    print(f"top_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"message_roles={dict(sorted(message_roles.items()))}")
    print(f"tool_names={dict(sorted(tool_names.items()))}")
    print("bounded_tool_argument_samples:")
    for index, sample in enumerate(command_samples, 1):
        print(f"  {index}: {sample}")
    print("assistant_messages:")
    for index, message in enumerate(final_messages, 1):
        bounded = message if len(message) <= 3000 else message[:3000] + "...[bounded]"
        print(f"  [{index}] {bounded}")


if __name__ == "__main__":
    main()
