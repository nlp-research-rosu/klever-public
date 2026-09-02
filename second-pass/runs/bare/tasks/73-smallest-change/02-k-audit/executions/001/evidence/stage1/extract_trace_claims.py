#!/usr/bin/env python3
"""Read every structured trace record and print bounded untrusted claims."""

from __future__ import annotations

from collections import Counter
import glob
import json


paths = sorted(glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True))
counts: Counter[tuple[str, str, str]] = Counter()
assistant_messages: list[str] = []
relevant_calls: list[str] = []
record_count = 0

needles = (
    "kompile",
    "kprove",
    "krun",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "random",
)

for path in paths:
    with open(path, encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record_count += 1
            record = json.loads(line)
            payload = record.get("payload", {})
            key = (
                str(record.get("type", "")),
                str(payload.get("type", "")),
                str(payload.get("role", "")),
            )
            counts[key] += 1

            if (
                record.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
            ):
                text = "\n".join(
                    item.get("text", "") for item in payload.get("content", [])
                )
                assistant_messages.append(text)

            if (
                record.get("type") == "response_item"
                and payload.get("type") == "custom_tool_call"
            ):
                call_text = str(payload.get("input", ""))
                if any(needle in call_text for needle in needles):
                    relevant_calls.append(
                        f"{payload.get('name', '')}: {call_text[:4000]}"
                    )

print(f"TRACE_FILES: {len(paths)}")
print(f"TRACE_RECORDS_PARSED: {record_count}")
print("RECORD_COUNTS:")
for key, count in sorted(counts.items()):
    print(f"  {count:4d} {key}")

print("ASSISTANT CLAIMS (UNTRUSTED):")
for index, message in enumerate(assistant_messages, 1):
    print(f"--- assistant message {index} ---")
    print(message)

print("RELEVANT TOOL CALL CLAIMS (UNTRUSTED, EACH TRUNCATED TO 4000 CHARS):")
for index, call in enumerate(relevant_calls, 1):
    print(f"--- call {index} ---")
    print(call)
