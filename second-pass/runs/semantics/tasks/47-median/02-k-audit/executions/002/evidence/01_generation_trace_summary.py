#!/usr/bin/env python3
"""Read the complete structured trace and summarize every tool interaction."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T23-55-07-019f8d53-cebf-7702-a14d-059eccafc63d.jsonl"
)
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def compact(text: str, limit: int = 800) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit] + f" … <{len(text) - limit} chars omitted>"


def main() -> int:
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    function_calls: dict[str, dict] = {}
    call_outputs: dict[str, str] = {}
    messages: list[tuple[int, str, str, str]] = []
    raw_lines = TRACE.read_text().splitlines()
    for number, raw in enumerate(raw_lines, 1):
        event = json.loads(raw)
        top_types[event.get("type", "<none>")] += 1
        payload = event.get("payload", {})
        payload_type = payload.get("type", "<none>") if isinstance(payload, dict) else "<nonobject>"
        payload_types[payload_type] += 1
        if payload_type == "function_call":
            call_id = payload.get("call_id", payload.get("id", f"line-{number}"))
            function_calls[call_id] = {
                "line": number,
                "name": payload.get("name", "<none>"),
                "arguments": payload.get("arguments", ""),
            }
        elif payload_type == "function_call_output":
            call_outputs[payload.get("call_id", f"line-{number}")] = payload.get("output", "")
        elif payload_type == "message":
            role = payload.get("role", "<none>")
            phase = payload.get("phase", "<none>")
            text_parts = [
                part.get("text", "")
                for part in payload.get("content", [])
                if isinstance(part, dict)
            ]
            messages.append((number, role, phase, "\n".join(text_parts)))
        elif payload_type == "agent_message":
            messages.append(
                (number, "assistant", payload.get("phase", "<none>"), payload.get("message", ""))
            )

    output_text = OUTPUT_LOG.read_text(errors="replace")
    top_count = len(re.findall(r"(?m)^#Top$", output_text))
    error_count = len(re.findall(r"(?m)^\[Error\]", output_text))
    print(f"TRACE path={TRACE}")
    print(f"TRACE lines={len(raw_lines)} bytes={TRACE.stat().st_size}")
    print(f"TRACE top_types={dict(sorted(top_types.items()))}")
    print(f"TRACE payload_types={dict(sorted(payload_types.items()))}")
    print(f"OUTPUT_LOG lines={len(output_text.splitlines())} bytes={OUTPUT_LOG.stat().st_size}")
    print(f"OUTPUT_LOG #Top_count={top_count}")
    print(f"OUTPUT_LOG error_line_count={error_count}")
    print(f"OUTPUT_LOG KPROVE_PASSED_count={output_text.count('RESULT: KPROVE_PASSED')}")

    print("MESSAGES_BEGIN")
    for line, role, phase, text in messages:
        print(f"MESSAGE line={line} role={role} phase={phase} text={compact(text)}")
    print("MESSAGES_END")

    print("FUNCTION_CALLS_BEGIN")
    for call_id, record in sorted(function_calls.items(), key=lambda item: item[1]["line"]):
        output = call_outputs.get(call_id, "<missing output>")
        exit_match = re.search(r"Process exited with code (\d+)", output)
        running_match = re.search(r"Process running with session ID (\d+)", output)
        if exit_match:
            disposition = f"exit={exit_match.group(1)}"
        elif running_match:
            disposition = f"running_session={running_match.group(1)}"
        else:
            disposition = "no_exit_marker"
        print(
            f"CALL line={record['line']} id={call_id} name={record['name']} "
            f"{disposition} args={compact(record['arguments'], 1200)} "
            f"output={compact(output, 1200)}"
        )
    print("FUNCTION_CALLS_END")
    missing_outputs = sorted(set(function_calls) - set(call_outputs))
    print(f"MISSING_FUNCTION_OUTPUTS={missing_outputs}")
    return 1 if missing_outputs else 0


if __name__ == "__main__":
    raise SystemExit(main())
