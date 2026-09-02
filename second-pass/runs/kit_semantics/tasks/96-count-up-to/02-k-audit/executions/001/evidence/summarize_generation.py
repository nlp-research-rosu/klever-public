#!/usr/bin/env python3
"""Validate and summarize the untrusted structured generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T01-30-39-019f97f7-fd2b-7d23-9c10-a2fa3527fded.jsonl"
)


def main() -> None:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    response_items: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    last_messages: list[tuple[int, str, str]] = []
    parse_errors: list[tuple[int, str]] = []

    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                obj = json.loads(line)
            except Exception as err:  # untrusted evidence: report, do not hide
                parse_errors.append((line_number, repr(err)))
                continue
            top_types[str(obj.get("type"))] += 1
            payload = obj.get("payload")
            if isinstance(payload, dict):
                item_type = str(payload.get("type"))
                payload_types[item_type] += 1
                if obj.get("type") == "response_item":
                    response_items[item_type] += 1
                if item_type in {"function_call", "custom_tool_call"}:
                    tool_names[str(payload.get("name"))] += 1
                if item_type in {"message", "agent_message", "user_message"}:
                    role = str(payload.get("role", item_type))
                    content = payload.get("content", payload.get("message"))
                    text_parts: list[str] = []
                    if isinstance(content, str):
                        text_parts.append(content)
                    if isinstance(content, list):
                        for part in content:
                            if isinstance(part, dict) and isinstance(
                                part.get("text"), str
                            ):
                                text_parts.append(part["text"])
                    if text_parts:
                        last_messages.append(
                            (line_number, role, "\n".join(text_parts))
                        )
                        last_messages = last_messages[-12:]

    print("trace_path:", TRACE)
    print("line_count:", sum(top_types.values()) + len(parse_errors))
    print("parse_errors:", parse_errors)
    print("top_level_types:", dict(sorted(top_types.items())))
    print("payload_types:", dict(sorted(payload_types.items())))
    print("response_item_types:", dict(sorted(response_items.items())))
    print("tool_names:", dict(sorted(tool_names.items())))
    print("last_text_messages:")
    for line_number, role, text in last_messages:
        compact = text if len(text) <= 1200 else text[:1200] + "...<truncated>"
        print(f"--- line={line_number} role={role} chars={len(text)}")
        print(compact)


if __name__ == "__main__":
    main()
