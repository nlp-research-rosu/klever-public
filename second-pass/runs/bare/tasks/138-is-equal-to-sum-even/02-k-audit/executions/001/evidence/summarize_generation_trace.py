#!/usr/bin/env python3
"""Bounded provenance summary of the untrusted structured generation trace."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T07-21-24-019f89c6-0973-7943-8ce6-9ee05af209a5.jsonl"
)


def one_line(text: str, limit: int = 500) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[:limit] + "…"


def main() -> None:
    counts: Counter[str] = Counter()
    command_count = 0
    assistant_messages: list[str] = []

    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            item_type = item.get("type", "<missing>")
            counts[item_type] += 1
            payload = item.get("payload", {})

            if item_type == "response_item" and payload.get("type") in {
                "custom_tool_call",
                "function_call",
            }:
                command_count += 1
                name = payload.get("name", "<missing>")
                raw_input = payload.get("input", payload.get("arguments", ""))
                print(
                    f"TOOL_CALL line={line_number} name={name} "
                    f"input={one_line(str(raw_input))}"
                )

            if (
                item_type == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
            ):
                texts = [
                    part.get("text", "")
                    for part in payload.get("content", [])
                    if isinstance(part, dict) and part.get("type") == "output_text"
                ]
                if texts:
                    assistant_messages.append(one_line(" ".join(texts), 1000))

    print(f"TRACE={TRACE}")
    print(f"COUNTS={dict(sorted(counts.items()))}")
    print(f"TOOL_CALL_COUNT={command_count}")
    print(f"ASSISTANT_MESSAGE_COUNT={len(assistant_messages)}")
    for index, message in enumerate(assistant_messages, 1):
        print(f"ASSISTANT_MESSAGE_{index}={message}")


if __name__ == "__main__":
    main()
