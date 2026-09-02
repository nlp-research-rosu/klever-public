#!/usr/bin/env python3
"""Parse every structured generation event and scan the full text log."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T05-05-33-019fad56-2d2f-7c02-935e-b6ec58c8eb2b.jsonl"
)
TEXT_LOG = Path("/generation-evidence/codex-output.log")


def main() -> None:
    type_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    calls: list[tuple[int, str, str]] = []
    outputs: list[tuple[int, str]] = []
    final_messages: list[tuple[int, str]] = []

    with TRACE.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            event = json.loads(line)
            event_type = event.get("type", "<missing>")
            type_counts[event_type] += 1
            payload = event.get("payload", {})
            payload_type = payload.get("type", "<missing>")
            payload_counts[payload_type] += 1
            if event_type == "response_item" and payload_type == "function_call":
                calls.append(
                    (
                        number,
                        str(payload.get("name")),
                        str(payload.get("arguments")),
                    )
                )
            elif (
                event_type == "response_item"
                and payload_type == "function_call_output"
            ):
                outputs.append((number, str(payload.get("output"))))
            elif event_type == "response_item" and payload_type == "message":
                if payload.get("role") == "assistant":
                    text = "\n".join(
                        str(item.get("text", ""))
                        for item in payload.get("content", [])
                        if isinstance(item, dict)
                    )
                    final_messages.append((number, text))

    print(f"TRACE_LINES_PARSED: {sum(type_counts.values())}")
    print(f"TRACE_TOP_LEVEL_TYPES: {dict(sorted(type_counts.items()))}")
    print(f"TRACE_PAYLOAD_TYPES: {dict(sorted(payload_counts.items()))}")
    print(f"FUNCTION_CALLS: {len(calls)}")
    print(f"FUNCTION_OUTPUTS: {len(outputs)}")
    print(f"ASSISTANT_MESSAGES: {len(final_messages)}")

    print("RELEVANT_GENERATION_CALLS:")
    for number, name, arguments in calls:
        if any(
            marker in arguments
            for marker in (
                "kompile",
                "kprove",
                "krun",
                "py2mpy",
                "differential_test",
                "prove.sh",
            )
        ):
            compact = arguments.replace("\n", "\\n")
            print(f"line={number} tool={name} arguments={compact[:900]}")

    print("RELEVANT_GENERATION_OUTPUTS:")
    for number, output in outputs:
        if any(
            marker in output
            for marker in (
                "#Top",
                "WarnStuckClaimState",
                "Process exited with code",
                "PASS:",
                "MISMATCH",
            )
        ):
            compact = output.replace("\n", "\\n")
            print(f"line={number} output={compact[:900]}")

    if final_messages:
        number, message = final_messages[-1]
        print(f"LAST_ASSISTANT_MESSAGE_LINE: {number}")
        print(message)

    text_line_count = 0
    marker_counts: Counter[str] = Counter()
    markers = [
        "kprove",
        "kompile",
        "krun",
        "#Top",
        "WarnStuckClaimState",
        "VALIDATED",
        "KPROVE_PASSED",
    ]
    with TEXT_LOG.open(encoding="utf-8", errors="strict") as stream:
        for text_line_count, line in enumerate(stream, 1):
            for marker in markers:
                if marker in line:
                    marker_counts[marker] += 1
    print(f"TEXT_LOG_LINES_SCANNED: {text_line_count}")
    print(f"TEXT_LOG_MARKER_COUNTS: {dict(marker_counts)}")


if __name__ == "__main__":
    main()
