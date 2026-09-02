#!/usr/bin/env python3
"""Summarize every structured generation trace event for audit inspection."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T01-23-30-019f8da4-b81d-7d42-972c-696eaae8c3fa.jsonl"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    events = []
    type_counts: Counter[str] = Counter()
    subtype_counts: Counter[str] = Counter()
    calls = []
    assistant_messages = []
    for line_number, line in enumerate(TRACE.open(), 1):
        event = json.loads(line)
        events.append(event)
        event_type = event.get("type", "")
        payload = event.get("payload", {})
        subtype = payload.get("type", "")
        type_counts[event_type] += 1
        subtype_counts[f"{event_type}/{subtype}"] += 1
        if event_type == "response_item" and subtype in {
            "function_call",
            "custom_tool_call",
        }:
            calls.append(
                {
                    "line": line_number,
                    "name": payload.get("name"),
                    "arguments_or_input": payload.get("arguments", payload.get("input", "")),
                }
            )
        if (
            event_type == "response_item"
            and subtype == "message"
            and payload.get("role") == "assistant"
        ):
            text = " ".join(
                item.get("text", "")
                for item in payload.get("content", [])
                if isinstance(item, dict)
            )
            assistant_messages.append({"line": line_number, "text": text})

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        TRACE,
    ]
    print(f"trace_events={len(events)}")
    print(f"event_type_counts={dict(sorted(type_counts.items()))}")
    print(f"event_subtype_counts={dict(sorted(subtype_counts.items()))}")
    print(f"tool_call_count={len(calls)}")
    for call in calls:
        rendered = str(call["arguments_or_input"]).replace("\n", "\\n")
        print(f"call line={call['line']} name={call['name']} payload={rendered}")
    print(f"assistant_message_count={len(assistant_messages)}")
    for message in assistant_messages:
        print(f"assistant line={message['line']} text={message['text'].replace(chr(10), ' ')}")
    for path in required:
        print(f"record path={path} bytes={path.stat().st_size} sha256={sha(path)}")
    print("RESULT=PARSED_ALL_TRACE_EVENTS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
