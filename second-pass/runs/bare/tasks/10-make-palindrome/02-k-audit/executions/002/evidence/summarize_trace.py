#!/usr/bin/env python3
"""Render the structured generation trace into a bounded reviewable summary."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def main() -> None:
    trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    counts: Counter[tuple[str, str]] = Counter()
    with trace.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            record = json.loads(line)
            payload = record.get("payload", {})
            record_type = record.get("type", "<missing>")
            subtype = payload.get("type", "<missing>")
            counts[(record_type, subtype)] += 1

            if record_type == "event_msg" and subtype in {
                "agent_message",
                "task_complete",
                "turn_aborted",
            }:
                print(
                    f"LINE {line_number} EVENT {subtype}: "
                    f"{payload.get('message', '')}"
                )

            if record_type != "response_item" or subtype not in {
                "function_call",
                "function_call_output",
                "custom_tool_call",
                "custom_tool_call_output",
                "message",
            }:
                continue
            role = payload.get("role", "")
            if role in {"developer", "user"}:
                continue
            name = payload.get("name", "")
            text = payload.get(
                "arguments", payload.get("output", payload.get("content", ""))
            )
            rendered = (
                text
                if isinstance(text, str)
                else json.dumps(text, ensure_ascii=False, sort_keys=True)
            )
            print(
                f"LINE {line_number} ITEM {subtype} {role} {name}: "
                f"{rendered[:1800]}"
            )

    print("COUNTS")
    for key, value in sorted(counts.items()):
        print(key, value)


if __name__ == "__main__":
    main()
