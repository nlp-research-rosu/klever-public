#!/usr/bin/env python3
"""Read every structured generation-trace event and print a bounded inventory."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 400) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    rendered = " ".join(rendered.split())
    return rendered if len(rendered) <= limit else rendered[:limit] + "…"


def main() -> int:
    files = sorted(path for path in TRACE_ROOT.rglob("*") if path.is_file())
    top = Counter()
    payloads = Counter()
    calls: list[tuple[int, str, str]] = []
    messages: list[tuple[int, str, str]] = []
    line_count = 0

    for path in files:
        with path.open() as stream:
            for line in stream:
                line_count += 1
                record = json.loads(line)
                top[str(record.get("type"))] += 1
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                payload_type = str(payload.get("type"))
                payloads[payload_type] += 1
                if payload_type == "function_call":
                    calls.append(
                        (
                            line_count,
                            str(payload.get("name")),
                            compact(payload.get("arguments"), 700),
                        )
                    )
                if payload_type == "message":
                    role = str(payload.get("role"))
                    content = payload.get("content")
                    messages.append((line_count, role, compact(content, 700)))
                if payload_type == "agent_message":
                    messages.append(
                        (
                            line_count,
                            "assistant/event",
                            compact(payload.get("message"), 700),
                        )
                    )

    print(f"files={len(files)} JSON_lines={line_count}")
    print(f"top_level={dict(sorted(top.items()))}")
    print(f"payload_types={dict(sorted(payloads.items()))}")
    print(f"function_calls={len(calls)}")
    for line_number, name, arguments in calls:
        print(f"  line={line_number} name={name} arguments={arguments}")
    print(f"messages={len(messages)}")
    for line_number, role, content in messages:
        print(f"  line={line_number} role={role} content={content}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
