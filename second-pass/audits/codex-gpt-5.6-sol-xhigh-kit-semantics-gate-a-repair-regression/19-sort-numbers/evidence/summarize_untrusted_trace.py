#!/usr/bin/env python3
"""Produce a bounded audit summary of an untrusted Codex JSONL trace."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path
from typing import Any


def flatten_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(flatten_text(item) for item in value)
    if isinstance(value, dict):
        if isinstance(value.get("text"), str):
            return value["text"]
        return json.dumps(value, ensure_ascii=True, sort_keys=True)
    return repr(value)


def bounded(text: str, limit: int = 700) -> str:
    text = text.replace("\x00", "<NUL>")
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + "\n...<bounded>...\n" + text[-half:]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: summarize_untrusted_trace.py TRACE.jsonl", file=sys.stderr)
        return 64

    path = Path(sys.argv[1])
    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        record = json.loads(line)
        records.append(record)
        type_counts[str(record.get("type"))] += 1
        payload = record.get("payload") or {}
        payload_counts[str(payload.get("type"))] += 1

    print(
        json.dumps(
            {
                "bytes": path.stat().st_size,
                "lines": len(records),
                "path": str(path),
                "record_types": dict(sorted(type_counts.items())),
                "payload_types": dict(sorted(payload_counts.items())),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )

    for index, record in enumerate(records):
        payload = record.get("payload") or {}
        payload_type = payload.get("type")
        role = payload.get("role")
        if payload_type == "message" and role == "assistant":
            print(f"\nASSISTANT_MESSAGE record={index}")
            print(bounded(flatten_text(payload.get("content")), 1600))
        elif payload_type in {"custom_tool_call", "function_call"}:
            print(
                "\nTOOL_CALL "
                + json.dumps(
                    {
                        "arguments": bounded(
                            flatten_text(
                                payload.get("input", payload.get("arguments", ""))
                            ),
                            1200,
                        ),
                        "call_id": payload.get("call_id"),
                        "name": payload.get("name"),
                        "record": index,
                    },
                    ensure_ascii=True,
                    sort_keys=True,
                )
            )
        elif payload_type in {"custom_tool_call_output", "function_call_output"}:
            output = flatten_text(payload.get("output", ""))
            signals = [
                signal
                for signal in (
                    "#Top",
                    "WarnStuckClaimState",
                    "EXIT_STATUS",
                    "Process exited with code 0",
                    "Process exited with code 1",
                )
                if signal in output
            ]
            print(
                "\nTOOL_OUTPUT "
                + json.dumps(
                    {
                        "call_id": payload.get("call_id"),
                        "chars": len(output),
                        "record": index,
                        "signals": signals,
                        "text": bounded(output),
                    },
                    ensure_ascii=True,
                    sort_keys=True,
                )
            )
        elif payload_type in {"task_started", "task_complete"}:
            print(
                "\nTASK_EVENT "
                + json.dumps(payload, ensure_ascii=True, sort_keys=True)
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
