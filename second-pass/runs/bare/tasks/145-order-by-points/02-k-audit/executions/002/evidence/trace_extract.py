#!/usr/bin/env python3
"""Render the complete JSONL generation trace into a compact textual ledger."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T07-31-48-019f89cf-8c90-7a01-99ba-8a917ae7dcf0.jsonl"
)


def truncate(text: str, limit: int = 1600) -> str:
    text = text.replace("\x1b", "<ESC>")
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[{len(text) - limit} characters omitted]..."


def main() -> int:
    outer = Counter()
    payload_types = Counter()
    total = 0
    with TRACE.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            total += 1
            item = json.loads(line)
            outer[item.get("type", "<missing>")] += 1
            payload = item.get("payload", {})
            payload_type = payload.get("type", "<missing>")
            payload_types[payload_type] += 1
            print(
                f"LINE {line_number} outer={item.get('type')} "
                f"payload={payload_type} time={item.get('timestamp')}"
            )

            if item.get("type") == "response_item":
                role = payload.get("role")
                if role:
                    print(f"  role={role}")
                if payload_type == "message":
                    chunks = payload.get("content", [])
                    texts = [
                        chunk.get("text", "")
                        for chunk in chunks
                        if isinstance(chunk, dict)
                        and chunk.get("type") in {"input_text", "output_text"}
                    ]
                    if role in {"user", "assistant"}:
                        print(truncate("\n".join(texts)))
                elif payload_type in {"function_call", "custom_tool_call"}:
                    print(
                        truncate(
                            f"  name={payload.get('name')} "
                            f"arguments={payload.get('arguments') or payload.get('input')}"
                        )
                    )
                elif payload_type in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    print(truncate(str(payload.get("output", ""))))
            elif item.get("type") == "event_msg":
                if payload_type in {
                    "agent_message",
                    "task_complete",
                    "turn_aborted",
                    "token_count",
                }:
                    print(truncate(json.dumps(payload, sort_keys=True)))

    print(f"parsed_lines={total}")
    print(f"outer_type_counts={dict(sorted(outer.items()))}")
    print(f"payload_type_counts={dict(sorted(payload_types.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
