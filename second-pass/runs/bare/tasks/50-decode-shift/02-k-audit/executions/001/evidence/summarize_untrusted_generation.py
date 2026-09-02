#!/usr/bin/env python3
"""Bounded structural summary of generation records, treated as untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-05-54-019f8949-f815-7ab2-914a-41c652141e1e.jsonl"
)
LOG = Path("/candidate/codex-output.log")


def main() -> int:
    event_types: collections.Counter[str] = collections.Counter()
    response_types: collections.Counter[str] = collections.Counter()
    event_msg_types: collections.Counter[str] = collections.Counter()
    command_claims: list[str] = []
    final_messages: list[str] = []
    invalid_json = 0

    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                invalid_json += 1
                continue
            outer_type = str(item.get("type"))
            event_types[outer_type] += 1
            payload = item.get("payload", {})
            if outer_type == "response_item":
                response_type = str(payload.get("type"))
                response_types[response_type] += 1
                if response_type in {"function_call", "custom_tool_call"}:
                    name = payload.get("name", payload.get("call_id", "<unnamed>"))
                    arguments = payload.get("arguments", payload.get("input", ""))
                    command_claims.append(f"{name}: {arguments}")
                if response_type == "message" and payload.get("role") == "assistant":
                    for content in payload.get("content", []):
                        if content.get("type") == "output_text":
                            final_messages.append(str(content.get("text", "")))
            elif outer_type == "event_msg":
                event_msg_types[str(payload.get("type"))] += 1

    patterns = [
        "#Top",
        "WarnStuckClaimState",
        "[Error]",
        "timed out",
        "timeout",
        "kprove spec.k",
        "kompile semantic.k",
        "krun solution.mpy",
        "spec-vacuity",
    ]
    pattern_counts = collections.Counter()
    with LOG.open(encoding="utf-8", errors="replace") as stream:
        log_lines = 0
        for line in stream:
            log_lines += 1
            for pattern in patterns:
                if pattern.lower() in line.lower():
                    pattern_counts[pattern] += 1

    print(f"trace={TRACE}")
    print(f"trace_invalid_json_lines={invalid_json}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_response_types={dict(sorted(response_types.items()))}")
    print(f"trace_event_msg_types={dict(sorted(event_msg_types.items()))}")
    print(f"trace_tool_call_count={len(command_claims)}")
    print("trace_tool_calls_first_20:")
    for command in command_claims[:20]:
        print(command[:800].replace("\n", "\\n"))
    print(f"assistant_message_count={len(final_messages)}")
    if final_messages:
        print("last_assistant_message:")
        print(final_messages[-1])
    print(f"codex_output_lines={log_lines}")
    print(f"codex_output_pattern_counts={dict(pattern_counts)}")
    print("interpretation=all values above are untrusted generation-record claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
