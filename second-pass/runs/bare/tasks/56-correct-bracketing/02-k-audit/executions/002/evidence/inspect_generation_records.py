#!/usr/bin/env python3
"""Traverse the complete generation log and structured trace, bounded output."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


def flatten_output(payload: dict) -> str:
    items = payload.get("output", [])
    if not isinstance(items, list):
        return str(items)
    parts: list[str] = []
    for item in items:
        if isinstance(item, dict):
            parts.append(str(item.get("text", "")))
        else:
            parts.append(str(item))
    return "".join(parts)


def one_line(text: str, limit: int = 500) -> str:
    normalized = " ".join(text.split())
    return normalized[:limit] + ("..." if len(normalized) > limit else "")


def main() -> None:
    root = Path("/generation-evidence")
    trace_files = sorted((root / "codex-trace").rglob("*.jsonl"))
    print(f"TRACE_FILES count={len(trace_files)}")
    type_counts: Counter[object] = Counter()
    payload_counts: Counter[object] = Counter()
    calls: dict[str, str] = {}
    completed_calls = 0
    total_lines = 0
    agent_messages: list[str] = []

    for trace_file in trace_files:
        for line_number, line in enumerate(trace_file.open(), 1):
            total_lines += 1
            record = json.loads(line)
            type_counts[record.get("type")] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = payload.get("type")
            payload_counts[payload_type] += 1
            if payload_type in {"custom_tool_call", "function_call"}:
                call_id = str(payload.get("call_id", payload.get("id", "")))
                call_text = str(
                    payload.get("input", payload.get("arguments", ""))
                )
                calls[call_id] = call_text
                print(
                    f"CALL line={line_number} id={call_id} "
                    f"name={payload.get('name')} input={one_line(call_text)}"
                )
            elif payload_type in {
                "custom_tool_call_output",
                "function_call_output",
            }:
                completed_calls += 1
                call_id = str(payload.get("call_id", ""))
                output = flatten_output(payload)
                signals = []
                for signal in (
                    "#Top",
                    "WarnStuckClaimState",
                    "timed out",
                    "failed",
                    "succeeded",
                ):
                    count = output.count(signal)
                    if count:
                        signals.append(f"{signal}={count}")
                print(
                    f"OUTPUT line={line_number} id={call_id} "
                    f"signals={','.join(signals) or 'none'} "
                    f"summary={one_line(output)}"
                )
            elif payload_type == "agent_message":
                message = str(payload.get("message", ""))
                agent_messages.append(message)
                print(
                    f"AGENT_MESSAGE line={line_number} "
                    f"phase={payload.get('phase')} text={one_line(message, 1000)}"
                )

    output_text = (root / "codex-output.log").read_text(
        encoding="utf-8", errors="replace"
    )
    output_lines = output_text.splitlines()
    print(f"TRACE_LINES count={total_lines}")
    print(f"TRACE_TOP_TYPES {dict(type_counts)}")
    print(f"TRACE_PAYLOAD_TYPES {dict(payload_counts)}")
    print(
        f"TRACE_CALLS started={len(calls)} completed_outputs={completed_calls}"
    )
    print(
        "CODEX_OUTPUT "
        f"lines={len(output_lines)} bytes={len(output_text.encode())} "
        f"top_markers={output_text.count('#Top')} "
        f"stuck_markers={output_text.count('WarnStuckClaimState')} "
        f"kprove_mentions={output_text.count('kprove spec.k')}"
    )
    print(f"AGENT_MESSAGES count={len(agent_messages)}")
    print(
        "FINAL_GENERATION_CLAIM "
        + one_line((root / "codex-last.txt").read_text(), 2000)
    )
    print("COMPLETE GENERATION RECORD TRAVERSAL OK")


if __name__ == "__main__":
    main()
