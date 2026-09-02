#!/usr/bin/env python3
"""Read and summarize every structured generation-trace event."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def bounded(value: object, limit: int = 600) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "\\0")
    if len(text) > limit:
        return text[:limit] + f"... <{len(text) - limit} chars omitted>"
    return text


def main() -> int:
    trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tools: collections.Counter[str] = collections.Counter()
    malformed: list[str] = []
    calls: list[tuple[int, str, str]] = []
    outputs: list[tuple[int, str]] = []
    messages: list[tuple[int, str, str]] = []
    total_lines = 0

    print(f"trace_files={len(trace_files)}")
    for path in trace_files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"trace_file={path.relative_to(TRACE_ROOT)} sha256={digest}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    event = json.loads(line)
                except Exception as error:
                    malformed.append(f"{path}:{line_number}: {error}")
                    continue
                event_type = str(event.get("type"))
                top_types[event_type] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type"))
                    payload_types[payload_type] += 1
                    if payload_type in {"custom_tool_call", "function_call"}:
                        name = str(payload.get("name"))
                        tools[name] += 1
                        calls.append(
                            (
                                line_number,
                                name,
                                bounded(payload.get("input", payload.get("arguments", ""))),
                            )
                        )
                    elif payload_type in {"custom_tool_call_output", "function_call_output"}:
                        outputs.append((line_number, bounded(payload.get("output", ""))))
                    elif payload_type == "message":
                        role = str(payload.get("role"))
                        messages.append((line_number, role, bounded(payload.get("content", ""))))
                    elif event_type == "event_msg" and payload_type in {
                        "agent_message",
                        "task_complete",
                    }:
                        messages.append((line_number, payload_type, bounded(payload)))

    print(f"total_jsonl_lines={total_lines}")
    print(f"malformed_lines={len(malformed)}")
    for item in malformed:
        print(f"MALFORMED {item}")
    print(f"top_level_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_names={dict(sorted(tools.items()))}")
    print(f"tool_calls={len(calls)} tool_outputs={len(outputs)} messages={len(messages)}")
    print("--- BOUNDED TOOL CALL INVENTORY ---")
    for line_number, name, data in calls:
        print(f"line={line_number} tool={name} input={data}")
    print("--- FINAL TRACE MESSAGES ---")
    for line_number, role, data in messages[-8:]:
        print(f"line={line_number} role={role} content={data}")

    raw = OUTPUT_LOG.read_bytes()
    decoded = raw.decode("utf-8")
    print("--- CODEX OUTPUT INTEGRITY ---")
    print(
        f"bytes={len(raw)} lines={len(decoded.splitlines())} "
        f"sha256={hashlib.sha256(raw).hexdigest()} nul_bytes={raw.count(bytes([0]))}"
    )
    markers = [
        "kprove ",
        "kompile ",
        "krun ",
        "#Top",
        "WarnStuckClaimState",
        "EXPECTED",
        "rotation oracle",
        "RESULT:",
    ]
    for marker in markers:
        print(f"marker={marker!r} count={decoded.count(marker)}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
