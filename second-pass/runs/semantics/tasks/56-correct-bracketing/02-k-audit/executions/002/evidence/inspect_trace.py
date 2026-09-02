#!/usr/bin/env python3
"""Parse every structured trace record and summarize the untrusted history."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T00-28-36-019f8d72-7511-7951-be00-bd7479873c9d.jsonl"
)


def main() -> None:
    outer: collections.Counter[str] = collections.Counter()
    inner: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    tool_calls: list[tuple[int, str]] = []
    parsed = 0
    with TRACE.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            parsed += 1
            outer[str(record.get("type"))] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            inner[str(payload.get("type"))] += 1
            if "role" in payload:
                roles[str(payload["role"])] += 1
            if payload.get("type") in ("function_call", "custom_tool_call"):
                tool_calls.append((line_number, str(payload.get("name"))))
    print(f"parsed_json_lines={parsed}")
    print(f"outer_types={dict(sorted(outer.items()))}")
    print(f"payload_types={dict(sorted(inner.items()))}")
    print(f"message_roles={dict(sorted(roles.items()))}")
    print(f"tool_call_count={len(tool_calls)}")
    print(f"first_tool_calls={tool_calls[:10]}")
    print(f"last_tool_calls={tool_calls[-10:]}")


if __name__ == "__main__":
    main()
