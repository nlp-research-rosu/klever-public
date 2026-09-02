#!/usr/bin/env python3
"""Read every JSONL trace record and emit a bounded structural inspection."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T03-40-29-019f986e-d932-7b33-b966-d8766d08175b.jsonl"
)


def flatten_message(payload: dict) -> str:
    parts: list[str] = []
    for item in payload.get("content", []):
        if isinstance(item, dict):
            text = item.get("text") or item.get("input_text") or item.get("output_text")
            if text:
                parts.append(str(text))
    return "\n".join(parts)


def bounded(text: str, limit: int = 1200) -> str:
    text = text.replace("\x00", "\\0")
    if len(text) <= limit:
        return text
    return text[:600] + f"\n... <{len(text) - 1200} chars omitted> ...\n" + text[-600:]


def main() -> int:
    outer = collections.Counter()
    response_types = collections.Counter()
    event_types = collections.Counter()
    records = []
    with TRACE.open() as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            records.append(item)
            outer[item.get("type")] += 1
            payload = item.get("payload", {})
            if item.get("type") == "response_item":
                response_types[payload.get("type")] += 1
            elif item.get("type") == "event_msg":
                event_types[payload.get("type")] += 1

    print(f"TRACE_PATH: {TRACE}")
    print(f"RECORDS_PARSED: {len(records)}")
    print(f"OUTER_TYPES: {dict(sorted(outer.items()))}")
    print(f"RESPONSE_TYPES: {dict(sorted(response_types.items()))}")
    print(f"EVENT_TYPES: {dict(sorted(event_types.items()))}")

    for index, item in enumerate(records, 1):
        payload = item.get("payload", {})
        if item.get("type") == "response_item":
            payload_type = payload.get("type")
            if payload_type == "message" and payload.get("role") == "assistant":
                print(
                    f"\nTRACE[{index}] ASSISTANT_MESSAGE:\n"
                    f"{bounded(flatten_message(payload), 2400)}"
                )
            elif payload_type in {"function_call", "custom_tool_call"}:
                name = payload.get("name") or payload.get("tool_name")
                arguments = payload.get("arguments") or payload.get("input") or ""
                print(
                    f"\nTRACE[{index}] TOOL_CALL name={name}:\n"
                    f"{bounded(str(arguments), 1600)}"
                )
            elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                output = payload.get("output") or ""
                output_text = output if isinstance(output, str) else json.dumps(output)
                status_lines = [
                    line
                    for line in output_text.splitlines()
                    if any(
                        needle in line
                        for needle in (
                            "Process exited with code",
                            "exit_code",
                            "EXIT_STATUS",
                            "#Top",
                            "WarnStuckClaimState",
                            "[Error]",
                            "RESULT:",
                        )
                    )
                ]
                if status_lines:
                    print(
                        f"\nTRACE[{index}] TOOL_OUTPUT_STATUS:\n"
                        + "\n".join(status_lines[:40])
                    )
        elif item.get("type") == "event_msg":
            event_type = payload.get("type")
            if event_type in {"task_complete", "turn_aborted", "token_count"}:
                print(
                    f"\nTRACE[{index}] EVENT {event_type}:\n"
                    f"{bounded(json.dumps(payload, sort_keys=True), 1600)}"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
