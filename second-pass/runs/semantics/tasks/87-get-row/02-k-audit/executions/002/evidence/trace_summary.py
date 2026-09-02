#!/usr/bin/env python3
"""Validate and summarize every record in the untrusted generation trace."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T02-48-31-019f8df2-8e3c-72e2-b4e0-c36fade90602.jsonl"
)
OUTPUT = Path("/generation-evidence/codex-output.log")


def short(text: str, limit: int = 800) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "...[bounded]"


def main() -> None:
    raw = TRACE.read_bytes()
    lines = raw.splitlines()
    top_types: Counter[str] = Counter()
    response_types: Counter[str] = Counter()
    calls: list[str] = []
    messages: list[str] = []

    for line_number, line in enumerate(lines, 1):
        record = json.loads(line)
        top_types[record.get("type", "<missing>")] += 1
        payload = record.get("payload", {})
        if record.get("type") == "response_item":
            subtype = payload.get("type", "<missing>")
            response_types[subtype] += 1
            if subtype in {"function_call", "custom_tool_call"}:
                name = payload.get("name", "<missing>")
                arguments = payload.get("arguments", payload.get("input", ""))
                calls.append(f"line={line_number} name={name} args={short(str(arguments))}")
            elif subtype == "message" and payload.get("role") == "assistant":
                parts = payload.get("content", [])
                text = " ".join(str(part.get("text", "")) for part in parts)
                messages.append(
                    f"line={line_number} phase={payload.get('phase')} text={short(text)}"
                )
        elif record.get("type") == "event_msg":
            subtype = payload.get("type", "<missing>")
            if subtype in {"agent_message", "task_complete"}:
                text = payload.get("message", payload.get("last_agent_message", ""))
                messages.append(f"line={line_number} event={subtype} text={short(str(text))}")

    output_raw = OUTPUT.read_bytes()
    output_text = output_raw.decode("utf-8")
    print(f"trace_sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"trace_lines_parsed={len(lines)}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_response_types={dict(sorted(response_types.items()))}")
    print(f"trace_function_calls={len(calls)}")
    for call in calls:
        print(call)
    print(f"trace_assistant_messages={len(messages)}")
    for message in messages:
        print(message)
    print(f"output_sha256={hashlib.sha256(output_raw).hexdigest()}")
    print(f"output_lines_read={len(output_text.splitlines())}")
    for needle in (
        "#Top",
        "KPROVE_PASSED",
        "WarnStuckClaimState",
        "verification.k",
        "spec.k",
        "addMatch",
    ):
        print(f"output_occurrences[{needle}]={output_text.count(needle)}")


if __name__ == "__main__":
    main()
