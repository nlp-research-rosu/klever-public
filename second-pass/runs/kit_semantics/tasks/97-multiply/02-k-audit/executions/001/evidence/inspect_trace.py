#!/usr/bin/env python3
"""Parse every generation trace event and emit a bounded event-by-event index."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T23-54-31-019fb15f-c44f-79f2-b9a7-61e9b417afbe.jsonl"
)


def squash(value: str, limit: int = 220) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 3] + "..."


def text_and_hash(value: str) -> str:
    digest = hashlib.sha256(value.encode()).hexdigest()[:12]
    return f"sha256={digest} text={squash(value)!r}"


def summarize(document: dict) -> str:
    event_type = document.get("type", "<missing>")
    payload = document.get("payload")
    if not isinstance(payload, dict):
        return f"type={event_type} payload={squash(repr(payload))}"

    payload_type = payload.get("type")
    prefix = f"type={event_type} payload_type={payload_type}"
    if event_type == "response_item":
        if payload_type == "function_call":
            return (
                f"{prefix} name={payload.get('name')} "
                f"arguments={squash(str(payload.get('arguments')), 500)}"
            )
        if payload_type == "function_call_output":
            output = payload.get("output", "")
            if not isinstance(output, str):
                output = json.dumps(output, sort_keys=True)
            return f"{prefix} {text_and_hash(output)}"
        if payload_type == "custom_tool_call":
            tool_input = payload.get("input", "")
            if not isinstance(tool_input, str):
                tool_input = json.dumps(tool_input, sort_keys=True)
            return (
                f"{prefix} name={payload.get('name')} "
                f"input={squash(tool_input, 500)!r}"
            )
        if payload_type == "custom_tool_call_output":
            output = payload.get("output", "")
            if not isinstance(output, str):
                output = json.dumps(output, sort_keys=True)
            return f"{prefix} {text_and_hash(output)}"
        if payload_type == "message":
            pieces: list[str] = []
            for item in payload.get("content", []):
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    pieces.append(item["text"])
            return (
                f"{prefix} role={payload.get('role')} "
                + text_and_hash("\n".join(pieces))
            )
        return f"{prefix} keys={sorted(payload)}"
    if event_type == "event_msg":
        if isinstance(payload.get("message"), str):
            return f"{prefix} {text_and_hash(payload['message'])}"
        return f"{prefix} keys={sorted(payload)}"
    if event_type == "session_meta":
        return (
            f"{prefix} session_id={payload.get('session_id')} "
            f"cwd={payload.get('cwd')} cli={payload.get('cli_version')}"
        )
    if event_type == "world_state":
        return f"{prefix} full={payload.get('full')} keys={sorted(payload)}"
    if event_type == "turn_context":
        return (
            f"{prefix} turn_id={payload.get('turn_id')} cwd={payload.get('cwd')} "
            f"model={payload.get('model')}"
        )
    return f"{prefix} keys={sorted(payload)}"


def main() -> int:
    type_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    parsed = 0
    with TRACE.open() as stream:
        for line_number, line in enumerate(stream, 1):
            document = json.loads(line)
            if not isinstance(document, dict):
                raise TypeError(f"line {line_number} is not an object")
            event_type = str(document.get("type", "<missing>"))
            payload = document.get("payload")
            payload_type = (
                str(payload.get("type", "<none>"))
                if isinstance(payload, dict)
                else "<non-object>"
            )
            type_counts[event_type] += 1
            payload_counts[f"{event_type}/{payload_type}"] += 1
            parsed += 1
            print(f"{line_number:03d} {summarize(document)}")
    print(f"PARSED_LINES: {parsed}")
    print("TYPE_COUNTS:", dict(sorted(type_counts.items())))
    print("PAYLOAD_COUNTS:", dict(sorted(payload_counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
