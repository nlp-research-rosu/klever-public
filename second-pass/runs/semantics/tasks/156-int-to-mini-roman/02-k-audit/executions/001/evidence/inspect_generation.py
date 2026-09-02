#!/usr/bin/env python3
"""Stream and summarize every structured generation record as untrusted evidence."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/26/"
    "rollout-2026-07-26T03-06-58-019f9d76-858f-7c51-9132-7d340c4216a9.jsonl"
)
OUTPUT = Path("/generation-evidence/codex-output.log")


def compact(text: str, limit: int = 700) -> str:
    text = text.replace("\r", "").strip()
    if len(text) <= limit:
        return text
    return text[: limit // 2] + "\n...[bounded excerpt]...\n" + text[-limit // 2 :]


def main() -> None:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    function_names: collections.Counter[str] = collections.Counter()
    calls: dict[str, tuple[str, str]] = {}
    proof_calls: list[tuple[int, str, str, str]] = []
    proof_outputs: list[tuple[int, str, str, str]] = []
    final_messages: list[str] = []
    timestamps: list[str] = []

    with TRACE.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            top_types[record.get("type", "<missing>")] += 1
            if "timestamp" in record:
                timestamps.append(record["timestamp"])
            payload = record.get("payload", {})
            payload_type = payload.get("type", "<missing>")
            payload_types[payload_type] += 1

            if payload_type in {"function_call", "custom_tool_call"}:
                name = payload.get("name", "<missing>")
                function_names[name] += 1
                call_id = payload.get("call_id", "<missing>")
                raw_args = payload.get("arguments", payload.get("input", ""))
                calls[call_id] = (name, raw_args)
                if name == "exec_command":
                    try:
                        command = json.loads(raw_args).get("cmd", "")
                    except (json.JSONDecodeError, AttributeError):
                        command = raw_args
                    if any(token in command for token in ("kompile", "kprove", "krun")):
                        proof_calls.append((line_number, call_id, name, command))

            if payload_type in {"function_call_output", "custom_tool_call_output"}:
                call_id = payload.get("call_id", "<missing>")
                if call_id in calls and calls[call_id][0] == "exec_command":
                    raw_args = calls[call_id][1]
                    try:
                        command = json.loads(raw_args).get("cmd", "")
                    except (json.JSONDecodeError, AttributeError):
                        command = raw_args
                    if any(token in command for token in ("kompile", "kprove", "krun")):
                        proof_outputs.append(
                            (
                                line_number,
                                call_id,
                                command,
                                str(payload.get("output", "")),
                            )
                        )

            if payload_type == "message" and payload.get("role") == "assistant":
                if payload.get("phase") == "final_answer":
                    pieces = [
                        piece.get("text", "")
                        for piece in payload.get("content", [])
                        if isinstance(piece, dict)
                    ]
                    final_messages.append("\n".join(pieces))

    output_text = OUTPUT.read_text(errors="replace")
    print(f"trace={TRACE}")
    print(f"trace_lines={sum(top_types.values())}")
    print(f"timestamp_first={timestamps[0] if timestamps else '<none>'}")
    print(f"timestamp_last={timestamps[-1] if timestamps else '<none>'}")
    print(f"top_record_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_call_counts={dict(sorted(function_names.items()))}")
    print(f"generation_output_bytes={OUTPUT.stat().st_size}")
    print(f"generation_output_lines={output_text.count(chr(10)) + 1}")
    for token in ("#Top", "WarnStuckClaimState", "KPROVE_PASSED", "PARTIAL", "BLOCKED"):
        print(f"generation_output_count[{token}]={output_text.count(token)}")

    print("\nK-related generation commands (claims only, not trusted):")
    for line_number, call_id, _name, command in proof_calls:
        print(f"TRACE_LINE={line_number} CALL_ID={call_id}")
        print(compact(command, 1600))

    print("\nCorresponding bounded tool outputs (claims only, not trusted):")
    for line_number, call_id, command, output in proof_outputs:
        print(f"TRACE_LINE={line_number} CALL_ID={call_id}")
        print(f"COMMAND={compact(command, 500)}")
        print(f"OUTPUT={compact(output, 1800)}")

    print("\nFinal assistant messages (claims only, not trusted):")
    for message in final_messages:
        print(compact(message, 2400))


if __name__ == "__main__":
    main()
