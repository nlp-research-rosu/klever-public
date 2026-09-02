#!/usr/bin/env python3
"""Extract bounded, human-readable claims from the untrusted generation trace."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def one_line(value: object, limit: int = 1200) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(rendered) > limit:
        return rendered[:limit] + "...<bounded>"
    return rendered


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} TRACE.jsonl", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    counts: dict[str, int] = {}
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            record_type = record.get("type", "<missing>")
            counts[record_type] = counts.get(record_type, 0) + 1
            payload = record.get("payload", {})
            payload_type = payload.get("type") if isinstance(payload, dict) else None
            if payload_type in {
                "agent_message",
                "message",
                "custom_tool_call",
                "custom_tool_call_output",
                "turn_aborted",
            }:
                if payload_type == "message":
                    selected = {
                        "role": payload.get("role"),
                        "phase": payload.get("phase"),
                        "content": payload.get("content"),
                    }
                elif payload_type == "custom_tool_call":
                    selected = {
                        "name": payload.get("name"),
                        "input": payload.get("input"),
                    }
                elif payload_type == "custom_tool_call_output":
                    selected = {
                        "call_id": payload.get("call_id"),
                        "output": payload.get("output"),
                    }
                else:
                    selected = payload
                print(f"line={line_number} type={payload_type} {one_line(selected)}")
    print("record_counts=" + one_line(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
