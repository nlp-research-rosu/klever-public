#!/usr/bin/env python3
"""Parse every generation trace record and summarize its untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def main() -> None:
    files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"TRACE_FILES: {len(files)}")
    total = 0
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    command_count = 0
    k_command_count = 0
    top_claim_count = 0
    nonzero_claim_count = 0
    final_messages: list[str] = []

    for path in files:
        print(f"TRACE_FILE: {path.relative_to(TRACE_ROOT)}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                total += 1
                top_types[str(record.get("type", "(missing)"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "(missing)"))] += 1
                    text = json.dumps(payload, sort_keys=True)
                    if "exec_command" in text or "shell_command" in text:
                        command_count += 1
                    if any(tool in text for tool in ("kompile", "kprove", "krun")):
                        k_command_count += 1
                    if "#Top" in text:
                        top_claim_count += 1
                    if "WarnStuckClaimState" in text:
                        nonzero_claim_count += 1
                    if payload.get("type") in {
                        "agent_message",
                        "assistant_message",
                    }:
                        content = payload.get("message") or payload.get("text")
                        if isinstance(content, str) and "RESULT:" in content:
                            final_messages.append(content)
                event = record.get("event_msg")
                if isinstance(event, dict):
                    payload_types[f"event:{event.get('type', '(missing)')}"] += 1

    print(f"TRACE_JSON_RECORDS_PARSED: {total}")
    print("TOP_LEVEL_TYPES:")
    for key, value in sorted(top_types.items()):
        print(f"  {key}: {value}")
    print("PAYLOAD_EVENT_TYPES:")
    for key, value in sorted(payload_types.items()):
        print(f"  {key}: {value}")
    print(f"RECORDS_MENTIONING_COMMAND_TOOL: {command_count}")
    print(f"RECORDS_MENTIONING_K_TOOLS: {k_command_count}")
    print(f"RECORDS_MENTIONING_TOP: {top_claim_count}")
    print(f"RECORDS_MENTIONING_STUCK_CLAIM: {nonzero_claim_count}")
    print(f"FINAL_RESULT_MESSAGES: {len(final_messages)}")
    for message in final_messages:
        print("FINAL_MESSAGE_BEGIN")
        print(message)
        print("FINAL_MESSAGE_END")


if __name__ == "__main__":
    main()
