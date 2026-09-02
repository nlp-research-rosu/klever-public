#!/usr/bin/env python3
"""Read the complete untrusted generation trace and summarize its claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-25-08-019f8924-a678-7523-92c2-c4d5490703c0.jsonl"
)


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> None:
    top_types = collections.Counter()
    nested_types = collections.Counter()
    commands = []
    claimed_outputs = []
    final_messages = []
    record_count = 0

    with TRACE.open(encoding="utf-8") as stream:
        for line in stream:
            record_count += 1
            record = json.loads(line)
            top_types[record.get("type", "<none>")] += 1
            for item in walk(record):
                item_type = item.get("type")
                if item_type:
                    nested_types[item_type] += 1
                if item.get("name") == "exec" and isinstance(item.get("input"), str):
                    commands.append(item["input"])
                message = item.get("message")
                if isinstance(message, str) and (
                    "#Top" in message or "KPROVE_PASSED" in message
                ):
                    final_messages.append(message)
                output = item.get("output")
                if isinstance(output, str) and (
                    "#Top" in output
                    or "WarnStuckClaimState" in output
                    or "exited " in output
                ):
                    claimed_outputs.append(output)

    print(f"TRACE: {TRACE}")
    print(f"RECORDS: {record_count}")
    print(f"TOP_LEVEL_TYPES: {dict(top_types)}")
    print(f"NESTED_TYPES: {dict(nested_types)}")
    print(f"EXEC_CALLS_FOUND: {len(commands)}")
    print(f"CLAIMED_RELEVANT_OUTPUTS_FOUND: {len(claimed_outputs)}")
    print(f"FINAL_OR_SUCCESS_MESSAGES_FOUND: {len(final_messages)}")
    print("RELEVANT_EXEC_CALLS:")
    for index, command in enumerate(commands, 1):
        if any(word in command for word in ("kompile", "krun", "kprove", "prove.sh")):
            compact = " ".join(command.split())
            print(f"  {index}: {compact[:1000]}")
    print("CLAIMED_OUTPUT_EXCERPTS:")
    for index, output in enumerate(claimed_outputs, 1):
        compact = "\n".join(output.splitlines()[:30])
        print(f"--- claimed output {index} ---")
        print(compact[:4000])
    print("FINAL_OR_SUCCESS_MESSAGE_EXCERPTS:")
    for index, message in enumerate(final_messages, 1):
        print(f"--- message {index} ---")
        print(message[:4000])


if __name__ == "__main__":
    main()
