#!/usr/bin/env python3
"""Validate every JSONL record and summarize the untrusted generation trace."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-59-10-019f897a-bd0d-74e1-a077-a58951068b7f.jsonl"
)


def compact(value: object, limit: int = 1600) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    rendered = rendered.replace("\n", "\\n")
    if len(rendered) > limit:
        return rendered[:limit] + f"... <{len(rendered) - limit} chars omitted>"
    return rendered


def main() -> int:
    outer = collections.Counter()
    payload_types = collections.Counter()
    calls: list[tuple[int, str, object]] = []
    messages: list[tuple[int, str, object]] = []
    malformed: list[str] = []
    raw = TRACE.read_bytes()

    for number, line in enumerate(raw.splitlines(), 1):
        try:
            record = json.loads(line)
        except ValueError as error:
            malformed.append(f"line {number}: {error}")
            continue
        outer[record.get("type", "<missing>")] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            ptype = payload.get("type", "<missing>")
            payload_types[ptype] += 1
            if ptype in {"custom_tool_call", "function_call"}:
                calls.append(
                    (
                        number,
                        str(payload.get("name", "<missing>")),
                        payload.get("input", payload.get("arguments")),
                    )
                )
            if ptype == "message":
                role = str(payload.get("role", "<missing>"))
                content = payload.get("content")
                messages.append((number, role, content))
            if ptype == "agent_message":
                messages.append((number, "agent_message", payload.get("message")))

    print(f"trace={TRACE}")
    print(f"bytes={len(raw)}")
    print(f"sha256_file={hashlib.sha256(raw).hexdigest()}")
    print(f"line_count={len(raw.splitlines())}")
    print(f"malformed_json_lines={len(malformed)}")
    for issue in malformed:
        print(issue)
    print(f"outer_types={dict(sorted(outer.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_call_count={len(calls)}")
    for number, name, value in calls:
        print(f"CALL line={number} name={name} input={compact(value)}")
    print(f"message_count={len(messages)}")
    for number, role, value in messages:
        print(f"MESSAGE line={number} role={role} content={compact(value, 1000)}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
