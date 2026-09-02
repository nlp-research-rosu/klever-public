#!/usr/bin/env python3
"""Parse every JSONL record and inventory generation actions and claims."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T06-36-59-019f8ec3-b7fe-7e51-9608-f9360a1ad504.jsonl"
)


def concise(text: str, limit: int = 500) -> str:
    text = text.replace("\r", "")
    if len(text) <= limit:
        return text
    return text[: limit // 2] + "\n...[bounded]...\n" + text[-limit // 2 :]


def main() -> int:
    counts: Counter[tuple[str, str]] = Counter()
    calls: dict[str, tuple[int, str, object]] = {}
    parsed = 0

    for line_no, line in enumerate(TRACE.open(), 1):
        record = json.loads(line)
        parsed += 1
        outer = record.get("type", "")
        payload = record.get("payload", {})
        inner = payload.get("type", "") if isinstance(payload, dict) else ""
        counts[(outer, inner)] += 1

        if outer == "session_meta":
            print(
                f"SESSION line={line_no} id={payload.get('session_id')} "
                f"cwd={payload.get('cwd')} cli={payload.get('cli_version')}"
            )
        elif outer == "turn_context":
            print(
                f"TURN_CONTEXT line={line_no} cwd={payload.get('cwd')} "
                f"model={payload.get('model')}"
            )
        elif outer == "event_msg" and inner in {
            "task_started",
            "task_complete",
            "agent_message",
            "user_message",
        }:
            text = payload.get("message", "")
            digest = hashlib.sha256(text.encode()).hexdigest() if text else "-"
            print(
                f"EVENT line={line_no} type={inner} text_sha256={digest}\n"
                f"{concise(text)}"
            )
        elif outer == "response_item" and inner == "function_call":
            call_id = payload.get("call_id", "")
            name = payload.get("name", "")
            arguments = payload.get("arguments", "")
            try:
                rendered_args = json.loads(arguments)
            except (TypeError, json.JSONDecodeError):
                rendered_args = arguments
            calls[call_id] = (line_no, name, rendered_args)
            print(
                f"CALL line={line_no} call_id={call_id} name={name}\n"
                f"{json.dumps(rendered_args, sort_keys=True, ensure_ascii=False)}"
            )
        elif outer == "response_item" and inner == "function_call_output":
            call_id = payload.get("call_id", "")
            output = payload.get("output", "")
            source = calls.get(call_id)
            print(
                f"CALL_OUTPUT line={line_no} call_id={call_id} source={source} "
                f"output_sha256={hashlib.sha256(output.encode()).hexdigest()}\n"
                f"{concise(output, 900)}"
            )
        elif outer == "response_item" and inner == "custom_tool_call":
            call_id = payload.get("call_id", "")
            name = payload.get("name", "")
            arguments = payload.get("input", "")
            calls[call_id] = (line_no, name, arguments)
            print(
                f"CUSTOM_CALL line={line_no} call_id={call_id} name={name}\n"
                f"{concise(arguments, 1200)}"
            )
        elif outer == "response_item" and inner == "custom_tool_call_output":
            call_id = payload.get("call_id", "")
            output = payload.get("output", "")
            print(
                f"CUSTOM_OUTPUT line={line_no} call_id={call_id} "
                f"source={calls.get(call_id)} "
                f"output_sha256={hashlib.sha256(output.encode()).hexdigest()}\n"
                f"{concise(output, 900)}"
            )

    print(f"PARSED_RECORDS: {parsed}")
    print("TYPE_COUNTS:")
    for key, count in sorted(counts.items()):
        print(f"  {key}: {count}")
    print(f"CALLS_SEEN: {len(calls)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
