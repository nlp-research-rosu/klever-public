#!/usr/bin/env python3
"""Project the untrusted generation JSONL into a bounded, reviewable record."""

from __future__ import annotations

import json
import pathlib
import sys


def clipped(value: object, limit: int = 4000) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    return text if len(text) <= limit else text[:limit] + "...<clipped>"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 2
    path = pathlib.Path(sys.argv[1])
    count = 0
    types: dict[str, int] = {}
    selected = 0
    with path.open(encoding="utf-8") as stream:
        for lineno, line in enumerate(stream, 1):
            count += 1
            record = json.loads(line)
            record_type = str(record.get("type", "<missing>"))
            types[record_type] = types.get(record_type, 0) + 1
            payload = record.get("payload", {})
            payload_type = payload.get("type", "")
            if record_type not in {"event_msg", "response_item"}:
                continue
            interesting = {
                "agent_message",
                "function_call",
                "function_call_output",
                "task_complete",
                "turn_aborted",
            }
            if payload_type not in interesting:
                continue
            selected += 1
            body = (
                payload.get("message")
                or payload.get("text")
                or payload.get("arguments")
                or payload.get("output")
                or ""
            )
            print(
                f"line={lineno}\ttimestamp={record.get('timestamp', '')}"
                f"\trecord={record_type}\tpayload={payload_type}"
                f"\tname={payload.get('name', '')}\tbody={clipped(body)}"
            )
    print(f"records={count}")
    print(f"record_types={json.dumps(types, sort_keys=True)}")
    print(f"selected={selected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
